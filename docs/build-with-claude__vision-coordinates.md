# Coordinates and bounding boxes

How Claude resizes images, and how to work with the pixel coordinates it returns for bounding boxes, points, and UI elements.

---

Claude can locate and label regions of an image (for example, returning bounding boxes for tables, form fields, chart elements, or UI components). This guide covers how Claude resizes images before processing them and how to work with the pixel coordinates it returns, so that boxes and points line up with your original image.

You'll need this for OCR pipelines, form extraction, chart parsing, UI element location, and any task where you act on a specific region of an image. For sending images, supported formats, and per-model resolution limits, see [Vision](/docs/en/build-with-claude/vision).

<Note>
  **Claude works best with absolute pixel coordinates.** Ask for them explicitly in your prompt. For example: *"Return the bounding box of each table as `[x1, y1, x2, y2]` (top-left and bottom-right corners) in pixel coordinates."* Claude does not work well when you ask for normalized coordinates, for example: *"Return bounding box coordinates between `0` and `1000`."* Always ask for pixel coordinates and normalize in your own code if you need to. To get coordinates as machine-readable JSON instead of prose, define a schema with [structured outputs](/docs/en/build-with-claude/structured-outputs), for example an object with an `[x1, y1, x2, y2]` array per detected element.
</Note>

Coordinates follow the standard image convention: the origin `(0, 0)` is the top-left corner of the image, with x increasing to the right and y increasing downward. The coordinates Claude returns are pixel positions in the image Claude sees: your image after Claude resizes it to fit the model's native resolution (see [How Claude resizes and pads images](#how-claude-resizes-and-pads-images)). To get coordinates you can use directly, either pre-resize your image so the coordinates map one-to-one onto the image you have (see [Resize your image before uploading](#resize-your-image-before-uploading)), or rescale the coordinates Claude returns (see [Rescale coordinates when you cannot pre-resize](#rescale-coordinates-when-you-cannot-pre-resize)).

<Note>
  Claude's spatial reasoning has limits (see [Limitations](/docs/en/build-with-claude/vision#limitations)). Coordinate accuracy is best when you state the expected coordinate format in your prompt and spot-check results visually before processing at scale. Small elements lose precision when an image is downscaled: for fine targets, crop the region of interest and send the crop (offset returned coordinates by the crop origin), or use a high-resolution-tier model. For [PDF support](/docs/en/build-with-claude/pdf-support), pages are rasterized to images server-side at dimensions you don't control, so the returned coordinates can't be reliably mapped back onto the page. To work with coordinates on PDF content, rasterize the pages to images yourself and use the pre-resize approach.
</Note>

## How Claude resizes and pads images

Claude finds the largest aspect-preserving size that satisfies both of the model's image limits:

1. **Edge limit:** neither side exceeds the maximum edge length (1568 px on the standard tier, 2576 px on the high-resolution tier).
2. **Visual token limit:** the image's token cost `⌈width / 28⌉ × ⌈height / 28⌉` does not exceed the model's visual token budget (1568 tokens on the standard tier, 4784 on the high-resolution tier).

See [Resolution and token cost](/docs/en/build-with-claude/vision#evaluate-image-size) for which models are in which tier.

For nearly all photos and screenshots, the visual token limit is what determines the final size. The edge limit takes over only for elongated images such as panoramas or tall phone screenshots. Compute the size with the [reference implementation](#resize-your-image-before-uploading) rather than scaling to the edge length by hand: a 1920×1080 screenshot resizes to 1456×819, not 1568×882, and assuming the edge limit puts every coordinate noticeably off target.

The token limit can also trigger a resize when neither side exceeds the edge limit. Overlooking this is the most common cause of misaligned coordinates. For example, an A4 page scanned at 130 DPI is 1075×1520 pixels: both sides are under 1568 px, but it costs `39 × 55 = 2145` visual tokens, so Claude resizes it to 924×1307.

<Note>
  This example assumes a model on the standard resolution tier. A high-resolution-tier model doesn't resize the same scan: 2145 tokens is within its 4784-token budget, so the coordinates it returns map directly onto the 1075×1520 original. Model tiers are listed in [Resolution and token cost](/docs/en/build-with-claude/vision#evaluate-image-size).
</Note>

Claude then pads every image, resized or not, up to the next multiple of 28 pixels on the bottom and right edges (924×1307 becomes 924×1316 in the example). The padding contains no content: Claude perceives the padded image, but the page content only ever occupies the un-padded resized region. **Always normalize or rescale by the resized dimensions, not the padded dimensions**; dividing by the padded dimensions scales every coordinate by a small amount.

## Resize your image before uploading

The most reliable approach is to resize your image yourself before uploading, so the image you have is exactly the image Claude sees and the coordinates Claude returns need no conversion.

First check which resolution tier your model is on (see [Resolution and token cost](/docs/en/build-with-claude/vision#evaluate-image-size)) and pass the matching edge and token limits. The following reference implementation computes the exact size Claude resizes an image to:

<CodeGroup>
  ```bash cURL
  # This reference implementation is local math that makes no API request, so
  # there's nothing to show for cURL. See the SDK tabs.
  ```

  ```bash CLI
  # This reference implementation is local math that makes no API request, so
  # there's nothing to show for the CLI. See the SDK tabs.
  ```

  ```python Python
  import math


  def count_image_tokens(width: int, height: int) -> int:
      """Visual tokens consumed by an image: one token per 28x28 pixel patch."""
      return math.ceil(width / 28) * math.ceil(height / 28)


  def resized_size(
      width: int,
      height: int,
      max_edge: int = 1568,
      max_tokens: int = 1568,
  ) -> tuple[int, int]:
      """The size Claude resizes an image to before padding.

      Defaults are for the standard resolution tier. For high-resolution-tier
      models, use max_edge=2576 and max_tokens=4784. Returns (width, height).
      Images that already fit within the limits are returned unchanged.
      """

      def fits(w: int, h: int) -> bool:
          return (
              math.ceil(w / 28) * 28 <= max_edge
              and math.ceil(h / 28) * 28 <= max_edge
              and count_image_tokens(w, h) <= max_tokens
          )

      if fits(width, height):
          return (width, height)
      if height > width:
          resized_h, resized_w = resized_size(height, width, max_edge, max_tokens)
          return (resized_w, resized_h)

      # Binary search along the long edge for the largest aspect-preserving
      # size that fits.
      aspect_ratio = width / height
      lo, hi = 1, width  # lo always fits; hi never fits
      while lo + 1 < hi:
          mid = (lo + hi) // 2
          if fits(mid, max(round(mid / aspect_ratio), 1)):
              lo = mid
          else:
              hi = mid
      return (lo, max(round(lo / aspect_ratio), 1))


  # The A4 example from "How Claude resizes and pads images":
  print(resized_size(1075, 1520))  # (924, 1307)

  # To apply the resize, use your image library, for example Pillow:
  # image.resize(resized_size(*image.size))
  ```

  ```typescript TypeScript
  /** Visual tokens consumed by an image: one token per 28x28 pixel patch. */
  function countImageTokens(width: number, height: number): number {
    return Math.ceil(width / 28) * Math.ceil(height / 28);
  }

  /**
   * Round half to even (banker's rounding), matching Python's round(). The
   * live API resolves exact .5 ties toward the even neighbor, so Math.round
   * (which rounds halves up) would compute a different size for some images.
   */
  function roundTiesToEven(value: number): number {
    const floor = Math.floor(value);
    if (value - floor !== 0.5) return Math.round(value);
    return floor % 2 === 0 ? floor : floor + 1;
  }

  /**
   * The size Claude resizes an image to before padding.
   *
   * Defaults are for the standard resolution tier. For high-resolution-tier
   * models, use maxEdge = 2576 and maxTokens = 4784. Returns [width, height].
   * Images that already fit within the limits are returned unchanged.
   */
  function resizedSize(
    width: number,
    height: number,
    maxEdge = 1568,
    maxTokens = 1568
  ): [number, number] {
    const fits = (w: number, h: number): boolean =>
      Math.ceil(w / 28) * 28 <= maxEdge &&
      Math.ceil(h / 28) * 28 <= maxEdge &&
      countImageTokens(w, h) <= maxTokens;

    if (fits(width, height)) return [width, height];
    if (height > width) {
      const [resizedH, resizedW] = resizedSize(height, width, maxEdge, maxTokens);
      return [resizedW, resizedH];
    }

    // Binary search along the long edge for the largest aspect-preserving
    // size that fits.
    const aspectRatio = width / height;
    let lo = 1; // lo always fits
    let hi = width; // hi never fits
    while (lo + 1 < hi) {
      const mid = Math.floor((lo + hi) / 2);
      if (fits(mid, Math.max(roundTiesToEven(mid / aspectRatio), 1))) {
        lo = mid;
      } else {
        hi = mid;
      }
    }
    return [lo, Math.max(roundTiesToEven(lo / aspectRatio), 1)];
  }

  // The A4 example from "How Claude resizes and pads images":
  console.log(resizedSize(1075, 1520)); // [ 924, 1307 ]

  // To apply the resize, use your image library, for example sharp:
  // await sharp(input).resize(width, height).toBuffer()
  ```

  ```csharp C#
  // Visual tokens consumed by an image: one token per 28x28 pixel patch.
  static int CountImageTokens(int width, int height)
  {
      return (width + 27) / 28 * ((height + 27) / 28); // ceil(w/28) * ceil(h/28)
  }

  // The size Claude resizes an image to before padding. Defaults are for the
  // standard resolution tier; for high-resolution-tier models, pass
  // maxEdge: 2576, maxTokens: 4784. Images that already fit within the limits
  // are returned unchanged.
  static (int Width, int Height) ResizedSize(
      int width, int height, int maxEdge = 1568, int maxTokens = 1568)
  {
      bool Fits(int w, int h) =>
          (w + 27) / 28 * 28 <= maxEdge
          && (h + 27) / 28 * 28 <= maxEdge
          && CountImageTokens(w, h) <= maxTokens;

      if (Fits(width, height))
      {
          return (width, height);
      }
      if (height > width)
      {
          (int resizedH, int resizedW) = ResizedSize(height, width, maxEdge, maxTokens);
          return (resizedW, resizedH);
      }

      // Binary search along the long edge for the largest aspect-preserving
      // size that fits. The short edge rounds half to even, matching the live
      // API at exact .5 ties (MidpointRounding.ToEven, Math.Round's default).
      double aspectRatio = (double)width / height;
      int lo = 1; // lo always fits
      int hi = width; // hi never fits
      while (lo + 1 < hi)
      {
          int mid = (lo + hi) / 2;
          if (Fits(mid, ShortEdge(mid)))
          {
              lo = mid;
          }
          else
          {
              hi = mid;
          }
      }
      return (lo, ShortEdge(lo));

      int ShortEdge(int longEdge) =>
          Math.Max((int)Math.Round(longEdge / aspectRatio, MidpointRounding.ToEven), 1);
  }

  // The A4 example from "How Claude resizes and pads images":
  Console.WriteLine(ResizedSize(1075, 1520)); // (924, 1307)
  ```

  ```go Go
  // countImageTokens is the visual tokens consumed by an image: one token per
  // 28x28 pixel patch.
  func countImageTokens(width, height int) int {
  	return ((width + 27) / 28) * ((height + 27) / 28) // ceil(w/28) * ceil(h/28)
  }

  // resizedSize is the size Claude resizes an image to before padding, as
  // (width, height). Pass maxEdge 1568 and maxTokens 1568 for the standard
  // resolution tier, or 2576 and 4784 for the high-resolution tier. Images
  // that already fit within the limits are returned unchanged.
  // The A4 example from "How Claude resizes and pads images":
  // resizedSize(1075, 1520, 1568, 1568) returns (924, 1307).
  func resizedSize(width, height, maxEdge, maxTokens int) (int, int) {
  	fits := func(w, h int) bool {
  		return ((w+27)/28)*28 <= maxEdge &&
  			((h+27)/28)*28 <= maxEdge &&
  			countImageTokens(w, h) <= maxTokens
  	}

  	if fits(width, height) {
  		return width, height
  	}
  	if height > width {
  		resizedH, resizedW := resizedSize(height, width, maxEdge, maxTokens)
  		return resizedW, resizedH
  	}

  	// Binary search along the long edge for the largest aspect-preserving
  	// size that fits. The short edge rounds half to even (math.RoundToEven),
  	// matching the live API at exact .5 ties; math.Round would round them up.
  	aspectRatio := float64(width) / float64(height)
  	lo, hi := 1, width // lo always fits; hi never fits
  	for lo+1 < hi {
  		mid := (lo + hi) / 2
  		short := max(int(math.RoundToEven(float64(mid)/aspectRatio)), 1)
  		if fits(mid, short) {
  			lo = mid
  		} else {
  			hi = mid
  		}
  	}
  	return lo, max(int(math.RoundToEven(float64(lo)/aspectRatio)), 1)
  }

  ```

  ```java Java
  /** A resized image size, as returned by resizedSize. */
  record Size(int width, int height) {}

  /** Visual tokens consumed by an image: one token per 28x28 pixel patch. */
  static int countImageTokens(int width, int height) {
      return Math.ceilDiv(width, 28) * Math.ceilDiv(height, 28);
  }

  /**
   * The size Claude resizes an image to before padding.
   *
   * <p>Pass maxEdge 1568 and maxTokens 1568 for the standard resolution tier,
   * or 2576 and 4784 for the high-resolution tier. Images that already fit
   * within the limits are returned unchanged.
   *
   * <p>The A4 example from "How Claude resizes and pads images":
   * resizedSize(1075, 1520, 1568, 1568) returns new Size(924, 1307).
   */
  static Size resizedSize(int width, int height, int maxEdge, int maxTokens) {
      if (fits(width, height, maxEdge, maxTokens)) {
          return new Size(width, height);
      }
      if (height > width) {
          Size rotated = resizedSize(height, width, maxEdge, maxTokens);
          return new Size(rotated.height(), rotated.width());
      }

      // Binary search along the long edge for the largest aspect-preserving
      // size that fits. The short edge rounds half to even (Math.rint),
      // matching the live API at exact .5 ties; Math.round would round them up.
      double aspectRatio = (double) width / height;
      int lo = 1; // lo always fits
      int hi = width; // hi never fits
      while (lo + 1 < hi) {
          int mid = (lo + hi) / 2;
          if (fits(mid, shortEdge(mid, aspectRatio), maxEdge, maxTokens)) {
              lo = mid;
          } else {
              hi = mid;
          }
      }
      return new Size(lo, shortEdge(lo, aspectRatio));
  }

  private static boolean fits(int width, int height, int maxEdge, int maxTokens) {
      return Math.ceilDiv(width, 28) * 28 <= maxEdge
              && Math.ceilDiv(height, 28) * 28 <= maxEdge
              && countImageTokens(width, height) <= maxTokens;
  }

  private static int shortEdge(int longEdge, double aspectRatio) {
      return Math.max((int) Math.rint(longEdge / aspectRatio), 1);
  }
  ```

  ```php PHP
  // Visual tokens consumed by an image: one token per 28x28 pixel patch.
  function countImageTokens(int $width, int $height): int
  {
      return intdiv($width + 27, 28) * intdiv($height + 27, 28);
  }

  /**
   * The size Claude resizes an image to before padding, as [width, height].
   *
   * Defaults are for the standard resolution tier. For high-resolution-tier
   * models, pass maxEdge: 2576, maxTokens: 4784. Images that already fit
   * within the limits are returned unchanged.
   */
  function resizedSize(int $width, int $height, int $maxEdge = 1568, int $maxTokens = 1568): array
  {
      $fits = fn (int $w, int $h): bool =>
          intdiv($w + 27, 28) * 28 <= $maxEdge
          && intdiv($h + 27, 28) * 28 <= $maxEdge
          && countImageTokens($w, $h) <= $maxTokens;

      if ($fits($width, $height)) {
          return [$width, $height];
      }
      if ($height > $width) {
          [$resizedH, $resizedW] = resizedSize($height, $width, $maxEdge, $maxTokens);
          return [$resizedW, $resizedH];
      }

      // Binary search along the long edge for the largest aspect-preserving
      // size that fits. The short edge rounds half to even
      // (PHP_ROUND_HALF_EVEN), matching the live API at exact .5 ties.
      $aspectRatio = $width / $height;
      $lo = 1; // lo always fits
      $hi = $width; // hi never fits
      while ($lo + 1 < $hi) {
          $mid = intdiv($lo + $hi, 2);
          $short = max((int) round($mid / $aspectRatio, 0, PHP_ROUND_HALF_EVEN), 1);
          if ($fits($mid, $short)) {
              $lo = $mid;
          } else {
              $hi = $mid;
          }
      }

      return [$lo, max((int) round($lo / $aspectRatio, 0, PHP_ROUND_HALF_EVEN), 1)];
  }

  // The A4 example from "How Claude resizes and pads images":
  [$resizedWidth, $resizedHeight] = resizedSize(1075, 1520);
  echo "({$resizedWidth}, {$resizedHeight})\n"; // (924, 1307)
  ```

  ```ruby Ruby
  # Visual tokens consumed by an image: one token per 28x28 pixel patch.
  def count_image_tokens(width, height)
    width.ceildiv(28) * height.ceildiv(28)
  end

  # The size Claude resizes an image to before padding, as [width, height].
  #
  # Defaults are for the standard resolution tier. For high-resolution-tier
  # models, pass max_edge: 2576, max_tokens: 4784. Images that already fit
  # within the limits are returned unchanged.
  def resized_size(width, height, max_edge = 1568, max_tokens = 1568)
    fits = lambda do |w, h|
      w.ceildiv(28) * 28 <= max_edge &&
        h.ceildiv(28) * 28 <= max_edge &&
        count_image_tokens(w, h) <= max_tokens
    end

    return [width, height] if fits.call(width, height)

    if height > width
      resized_h, resized_w = resized_size(height, width, max_edge, max_tokens)
      return [resized_w, resized_h]
    end

    # Binary search along the long edge for the largest aspect-preserving
    # size that fits. The short edge rounds half to even (round(half: :even)),
    # matching the live API at exact .5 ties.
    aspect_ratio = width.fdiv(height)
    lo = 1      # lo always fits
    hi = width  # hi never fits
    while lo + 1 < hi
      mid = (lo + hi) / 2
      short = [(mid / aspect_ratio).round(half: :even), 1].max
      if fits.call(mid, short)
        lo = mid
      else
        hi = mid
      end
    end

    [lo, [(lo / aspect_ratio).round(half: :even), 1].max]
  end

  # The A4 example from "How Claude resizes and pads images":
  p resized_size(1075, 1520) # => [924, 1307]
  ```
</CodeGroup>

1. Resize the image to the dimensions returned by the resize helper. If the image already fits within the model's limits, the helper returns its dimensions unchanged and no resize is needed.
2. [Send the resized image](/docs/en/build-with-claude/vision#send-images-to-claude) to the API. Don't pad it yourself. Claude handles padding, and padding doesn't shift the coordinate origin.
3. In your prompt, ask explicitly for pixel coordinates. For example: *"Return the click point for the Submit button as `[x, y]` in pixel coordinates."*
4. Use the returned coordinates directly against the image you sent. If you need normalized coordinates, divide by the dimensions of the image you sent, not by the original image's dimensions and not by the padded dimensions.

<Note>
  The [Token counting](/docs/en/build-with-claude/token-counting) endpoint estimates an image's token cost from its dimensions without fully processing it, so a successful count doesn't mean the image is within the Messages API's [request limits](/docs/en/build-with-claude/vision#request-limits). An image can count successfully and still be rejected when you send it.
</Note>

## Rescale coordinates when you cannot pre-resize

If you cannot pre-resize (for example, when the image comes from an upstream system you can't modify), use the resize helper from [Resize your image before uploading](#resize-your-image-before-uploading) to recover the dimensions Claude saw, then map the coordinates Claude returns into normalized coordinates or back onto your original image. Claude resizes oversized images rather than rejecting them, up to the API's [request limits](/docs/en/build-with-claude/vision#request-limits). Beyond those limits the request fails with a validation error instead. Pass the tier limits that match the model you called: the wrong tier's limits recover the wrong resized dimensions and silently shift every coordinate. This approach requires knowing the pixel dimensions of the image you uploaded, so it does not apply to PDF uploads.

<CodeGroup>
  ```bash cURL
  # This local coordinate conversion makes no API request, so there's nothing
  # to show for cURL. See the SDK tabs.
  ```

  ```bash CLI
  # This local coordinate conversion makes no API request, so there's nothing
  # to show for the CLI. See the SDK tabs.
  ```

  ```python Python
  # This helper calls resized_size from the resize example on this page.
  def to_relative_coordinates(
      x: float,
      y: float,
      original_width: int,
      original_height: int,
      max_edge: int = 1568,
      max_tokens: int = 1568,
  ) -> tuple[float, float]:
      """Map a pixel coordinate returned by Claude to relative coordinates in [0, 1].

      Pass the dimensions of the image you uploaded. For high-resolution-tier
      models, use max_edge=2576 and max_tokens=4784.
      """
      resized_w, resized_h = resized_size(
          original_width, original_height, max_edge, max_tokens
      )
      return (x / resized_w, y / resized_h)


  # A table corner Claude returns at (462, 653.5) on the resized A4 page maps
  # back onto the 1075x1520 original like this:
  rel_x, rel_y = to_relative_coordinates(462, 653.5, 1075, 1520)
  print((rel_x * 1075, rel_y * 1520))  # (537.5, 760.0)
  ```

  ```typescript TypeScript
  // This helper calls resizedSize from the resize example on this page.
  /**
   * Map a pixel coordinate returned by Claude to relative coordinates in [0, 1].
   *
   * Pass the dimensions of the image you uploaded. For high-resolution-tier
   * models, use maxEdge = 2576 and maxTokens = 4784.
   */
  function toRelativeCoordinates(
    x: number,
    y: number,
    originalWidth: number,
    originalHeight: number,
    maxEdge = 1568,
    maxTokens = 1568
  ): [number, number] {
    const [resizedW, resizedH] = resizedSize(
      originalWidth,
      originalHeight,
      maxEdge,
      maxTokens
    );
    return [x / resizedW, y / resizedH];
  }

  // A table corner Claude returns at (462, 653.5) on the resized A4 page maps
  // back onto the 1075x1520 original like this:
  const [relX, relY] = toRelativeCoordinates(462, 653.5, 1075, 1520);
  console.log([relX * 1075, relY * 1520]); // [ 537.5, 760 ]
  ```

  ```csharp C#
  // This helper calls ResizedSize from the resize example on this page.
  // Map a pixel coordinate returned by Claude to relative coordinates in
  // [0, 1]. Pass the dimensions of the image you uploaded, and the same tier
  // limits used for ResizedSize.
  static (double X, double Y) ToRelativeCoordinates(
      double x, double y, int originalWidth, int originalHeight,
      int maxEdge = 1568, int maxTokens = 1568)
  {
      (int resizedW, int resizedH) =
          ResizedSize(originalWidth, originalHeight, maxEdge, maxTokens);
      return (x / resizedW, y / resizedH);
  }

  // A table corner Claude returns at (462, 653.5) on the resized A4 page maps
  // back onto the 1075x1520 original like this:
  (double relX, double relY) = ToRelativeCoordinates(462, 653.5, 1075, 1520);
  Console.WriteLine((relX * 1075, relY * 1520)); // (537.5, 760)
  ```

  ```go Go
  // This helper calls resizedSize from the resize example on this page.

  // toRelativeCoordinates maps a pixel coordinate returned by Claude to
  // relative coordinates in [0, 1]. Pass the dimensions of the image you
  // uploaded, and the same tier limits used for resizedSize.
  func toRelativeCoordinates(
  	x, y float64,
  	originalWidth, originalHeight, maxEdge, maxTokens int,
  ) (float64, float64) {
  	resizedW, resizedH := resizedSize(originalWidth, originalHeight, maxEdge, maxTokens)
  	return x / float64(resizedW), y / float64(resizedH)
  }

  // To map back to your original image's pixel space, multiply by the original
  // dimensions: a table corner returned at (462, 653.5) on the resized A4 page
  // is (relX*1075, relY*1520) = (537.5, 760) on the 1075x1520 original.
  ```

  ```java Java
  // This helper calls resizedSize from the resize example on this page.
  /** A coordinate scaled into the [0, 1] range on both axes. */
  record RelativeCoordinate(double x, double y) {}

  /**
   * Map a pixel coordinate returned by Claude to relative coordinates in
   * [0, 1]. Pass the dimensions of the image you uploaded, and the same tier
   * limits used for resizedSize.
   */
  static RelativeCoordinate toRelativeCoordinates(
          double x, double y, int originalWidth, int originalHeight, int maxEdge, int maxTokens) {
      Size resized = resizedSize(originalWidth, originalHeight, maxEdge, maxTokens);
      return new RelativeCoordinate(x / resized.width(), y / resized.height());
  }

  // To map back to your original image's pixel space, multiply by the original
  // dimensions: a table corner returned at (462, 653.5) on the resized A4 page
  // is (relative.x() * 1075, relative.y() * 1520) = (537.5, 760) on the
  // 1075x1520 original.
  ```

  ```php PHP
  // This helper calls resizedSize() from the resize example on this page.
  /**
   * Map a pixel coordinate returned by Claude to relative coordinates in
   * [0, 1], as [x, y]. Pass the dimensions of the image you uploaded, and the
   * same tier limits used for resizedSize.
   */
  function toRelativeCoordinates(
      float $x,
      float $y,
      int $originalWidth,
      int $originalHeight,
      int $maxEdge = 1568,
      int $maxTokens = 1568,
  ): array {
      [$resizedW, $resizedH] = resizedSize($originalWidth, $originalHeight, $maxEdge, $maxTokens);

      return [$x / $resizedW, $y / $resizedH];
  }

  // A table corner Claude returns at (462, 653.5) on the resized A4 page maps
  // back onto the 1075x1520 original like this:
  [$relX, $relY] = toRelativeCoordinates(462, 653.5, 1075, 1520);
  echo '(' . $relX * 1075 . ', ' . $relY * 1520 . ")\n"; // (537.5, 760)
  ```

  ```ruby Ruby
  # This helper calls resized_size from the resize example on this page.
  # Map a pixel coordinate returned by Claude to relative coordinates in
  # [0, 1], as [x, y]. Pass the dimensions of the image you uploaded, and the
  # same tier limits used for resized_size.
  def to_relative_coordinates(
    x, y, original_width, original_height, max_edge = 1568, max_tokens = 1568
  )
    resized_w, resized_h = resized_size(original_width, original_height, max_edge, max_tokens)
    [x.fdiv(resized_w), y.fdiv(resized_h)]
  end

  # A table corner Claude returns at (462, 653.5) on the resized A4 page maps
  # back onto the 1075x1520 original like this:
  rel_x, rel_y = to_relative_coordinates(462, 653.5, 1075, 1520)
  p [rel_x * 1075, rel_y * 1520] # => [537.5, 760.0]
  ```
</CodeGroup>

Padding is applied only to the bottom and right edges, so the origin doesn't shift and a per-axis linear rescale is sufficient. Clamp returned coordinates to the resized dimensions before rescaling, so a point slightly outside the image can't map outside your original.

The relative coordinates multiply against whatever surface you act on: the original image, a full-resolution scan, or a screen. When you act on a screen and screenshot pixels differ from logical coordinates (HiDPI displays), also divide by the display scale factor. The [Computer use tool's scaling guidance](/docs/en/agents-and-tools/tool-use/computer-use-tool#handle-coordinate-scaling-for-higher-resolutions) covers that pattern.

## Next steps

<CardGroup cols={2}>
  <Card title="Agent Skills" icon="stack" href="/docs/en/agents-and-tools/agent-skills/overview">
    Agent Skills are modular capabilities that extend Claude's functionality. Each Skill packages instructions, metadata, and optional resources (scripts, templates) that Claude uses automatically when relevant.
  </Card>

  <Card title="Computer use tool" icon="computer" href="/docs/en/agents-and-tools/tool-use/computer-use-tool">
    Give Claude screenshot, mouse, and keyboard control of a desktop environment with the computer use tool.
  </Card>

  <Card title="PDF support" icon="file" href="/docs/en/build-with-claude/pdf-support">
    Process PDFs with Claude. Extract text, analyze charts, and understand visual content from your documents.
  </Card>

  <Card title="Token counting" icon="calculator" href="/docs/en/build-with-claude/token-counting">
    Count the tokens in a message before you send it to Claude. Use token counts to manage rate limits and costs, make model routing decisions, and fit prompts to a target length.
  </Card>
</CardGroup>
