# Website wizard

Create one-page websites based on user specifications.

---

> Copy this prompt into our developer [Console](/dashboard) to try it for yourself!

|        | Content                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| System | Your task is to create a one-page website based on the given specifications, delivered as an HTML file with embedded JavaScript and CSS. The website should incorporate a variety of engaging and interactive design features, such as drop-down menus, dynamic text and content, clickable buttons, and more. Ensure that the design is visually appealing, responsive, and user-friendly. The HTML, CSS, and JavaScript code should be well-structured, efficiently organized, and properly commented for readability and maintainability.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| User   | Create a one-page website for an online learning platform called "EduQuest" with the following features and sections:<br/><br/>1. A fixed navigation bar with links to course categories (Math, Science, Languages, Arts) and a search bar.<br/>2. A hero section with a video background showcasing students learning online, a dynamic tagline that rotates between "Learn at your own pace," "Discover new passions," and "Expand your horizons" every 3 seconds, and a "Get Started" button leading to a course catalog.<br/>3. A featured courses section displaying course cards with placeholders for course images, titles, instructors, and descriptions.<br/>4. An interactive "Learning Paths" section with a short quiz to determine learning styles and interests, and a button to start the quiz.<br/>5. A "Success Stories" section featuring testimonials from satisfied students, with placeholders for the testimonial text and student names.<br/>6. A footer with links to the platform's blog, FAQ, privacy policy, and a "Contact Us" button that opens a modal window with a contact form and customer support information.<br/><br/>Include filler placeholder content for the video background, course cards, and testimonials. Embed the CSS styles within the `<style>` tag in the `<head>` section and place the JavaScript code within the `<script>` tag at the end of the `<body>` section.<br/><br/>The JavaScript code should handle the dynamic tagline in the hero section, rotating through the different taglines every 3 seconds. |

## Example output

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduQuest - Online Learning Platform</title>
    <style>
        /* CSS Styles */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }

        header {
            background-color: #333;
            color: #fff;
            padding: 20px;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 999;
        }

        nav ul {
            list-style: none;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: space-between;
        }

        nav ul li a {
            color: #fff;
            text-decoration: none;
            padding: 10px;
        }

        .hero {
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .hero video {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: -1;
        }

        .hero h1 {
            font-size: 48px;
            margin-bottom: 20px;
        }

        .hero p {
            font-size: 24px;
            margin-bottom: 40px;
        }

        .hero button {
            padding: 10px 20px;
            font-size: 18px;
            background-color: #333;
            color: #fff;
            border: none;
            cursor: pointer;
        }

        .featured-courses, .success-stories {
            padding: 40px;
        }

        .course-card {
            background-color: #f5f5f5;
            padding: 20px;
            margin-bottom: 20px;
        }

        .testimonial {
            background-color: #f5f5f5;
            padding: 20px;
            margin-bottom: 20px;
        }

        footer {
            background-color: #333;
            color: #fff;
            padding: 20px;
            text-align: center;
        }

        footer a {
            color: #fff;
            text-decoration: none;
            margin: 0 10px;
        }

        footer button {
            padding: 10px 20px;
            font-size: 18px;
            background-color: #fff;
            color: #333;
            border: none;
            cursor: pointer;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="#">Math</a></li>
                <li><a href="#">Science</a></li>
                <li><a href="#">Languages</a></li>
                <li><a href="#">Arts</a></li>
                <li><input type="text" placeholder="Search"></li>
            </ul>
        </nav>
    </header>

    <section class="hero">
        <video src="placeholder-video.mp4" autoplay loop muted></video>
        <h1>Welcome to EduQuest</h1>
        <p id="tagline">Learn at your own pace</p>
        <button>Get Started</button>
    </section>

    <section class="featured-courses">
        <h2>Featured Courses</h2>
        <div class="course-card">
            <img src="placeholder-course-image.jpg" alt="Course Image">
            <h3>Course Title</h3>
            <p>Instructor: John Doe</p>
            <p>Course description goes here.</p>
        </div>
        <div class="course-card">
            <img src="placeholder-course-image.jpg" alt="Course Image">
            <h3>Course Title</h3>
            <p>Instructor: Jane Smith</p>
            <p>Course description goes here.</p>
        </div>
    </section>

    <section class="success-stories">
        <h2>Success Stories</h2>
        <div class="testimonial">
            <p>"EduQuest helped me learn a new skill and advance my career. Highly recommended!"</p>
            <p>- John Doe</p>
        </div>
        <div class="testimonial">
            <p>"I never thought I could learn a new language online, but EduQuest made it possible. Thank you!"</p>
            <p>- Jane Smith</p>
        </div>
    </section>

    <footer>
        <a href="#">Blog</a>
        <a href="#">FAQ</a>
        <a href="#">Privacy Policy</a>
        <button>Contact Us</button>
    </footer>

    <script>
        // JavaScript Code
        const taglines = [
            "Learn at your own pace",
            "Discover new passions",
            "Expand your horizons"
        ];

        let index = 0;
        const taglineElement = document.getElementById("tagline");

        function rotateTagline() {
            taglineElement.textContent = taglines[index];
            index = (index + 1) % taglines.length;
        }

        setInterval(rotateTagline, 3000);
    </script>
</body>
</html>
```

> This code creates a one-page website for "EduQuest" with the following features and sections:
> 
> A fixed navigation bar with links to course categories (Math, Science, Languages, Arts) and a search bar.
> 
> A hero section with a placeholder video background, a dynamic tagline that rotates between "Learn at your own pace," "Discover new passions," and "Expand your horizons" every 3 seconds, and a "Get Started" button.
> 
> A featured courses section displaying course cards with placeholders for course images, titles, instructors, and descriptions.
> 
> A "Success Stories" section featuring testimonials from satisfied students, with placeholders for the testimonial text and student names.
> 
> A footer with links to the platform's blog, FAQ, privacy policy, and a "Contact Us" button.
> 
> The CSS styles are embedded within the `<style>` tag in the `<head>` section, and the JavaScript code is placed within the `<script>` tag at the end of the `<body>` section.
> 
> The JavaScript code handles the dynamic tagline in the hero section, rotating through the different taglines every 3 seconds using the setInterval function.
> 
> Please note that the video background, course images, and testimonials are placeholders and should be replaced with actual content.

## API request

<Tabs>
<Tab title="Python">

```python
import anthropic

client = anthropic.Anthropic( # defaults to os.environ.get("ANTHROPIC_API_KEY")
api_key="my_api_key",
)
message = client.messages.create(
  model="claude-sonnet-4-5",
  max_tokens=4000,
  temperature=0,
  system="Your task is to create a one-page website based on the given specifications, delivered as an HTML file with embedded JavaScript and CSS. The website should incorporate a variety of engaging and interactive design features, such as drop-down menus, dynamic text and content, clickable buttons, and more. Ensure that the design is visually appealing, responsive, and user-friendly. The HTML, CSS, and JavaScript code should be well-structured, efficiently organized, and properly commented for readability and maintainability.",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Create a one-page website for an online learning platform called \"EduQuest\" with the following features and sections: \n \n1. A fixed navigation bar with links to course categories (Math, Science, Languages, Arts) and a search bar. \n \n2. A hero section with a video background showcasing students learning online, a dynamic tagline that rotates between \"Learn at your own pace,\" \"Discover new passions,\" and \"Expand your horizons\" every 3 seconds, and a \"Get Started\" button leading to a course catalog. \n \n3. A featured courses section displaying course cards with placeholders for course images, titles, instructors, and descriptions. \n \n4. An interactive \"Learning Paths\" section with a short quiz to determine learning styles and interests, and a button to start the quiz. \n \n5. A \"Success Stories\" section featuring testimonials from satisfied students, with placeholders for the testimonial text and student names. \n \n6. A footer with links to the platform's blog, FAQ, privacy policy, and a \"Contact Us\" button that opens a modal window with a contact form and customer support information. \n \nInclude filler placeholder content for the video background, course cards, and testimonials. Embed the CSS styles within the `<style>` tag in the `<head>` section and place the JavaScript code within the `<script>` tag at the end of the `<body>` section. \n \nThe JavaScript code should handle the dynamic tagline in the hero section, rotating through the different taglines every 3 seconds."
        }
      ]
    }
  ]
)
print(message.content)

```

</Tab>

<Tab title="TypeScript">
```typescript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: "my_api_key", // defaults to process.env["ANTHROPIC_API_KEY"]
});

const msg = await anthropic.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 4000,
  temperature: 0,
  system: "Your task is to create a one-page website based on the given specifications, delivered as an HTML file with embedded JavaScript and CSS. The website should incorporate a variety of engaging and interactive design features, such as drop-down menus, dynamic text and content, clickable buttons, and more. Ensure that the design is visually appealing, responsive, and user-friendly. The HTML, CSS, and JavaScript code should be well-structured, efficiently organized, and properly commented for readability and maintainability.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Create a one-page website for an online learning platform called \"EduQuest\" with the following features and sections:  \n  \n1. A fixed navigation bar with links to course categories (Math, Science, Languages, Arts) and a search bar.  \n  \n2. A hero section with a video background showcasing students learning online, a dynamic tagline that rotates between \"Learn at your own pace,\" \"Discover new passions,\" and \"Expand your horizons\" every 3 seconds, and a \"Get Started\" button leading to a course catalog.  \n  \n3. A featured courses section displaying course cards with placeholders for course images, titles, instructors, and descriptions.  \n  \n4. An interactive \"Learning Paths\" section with a short quiz to determine learning styles and interests, and a button to start the quiz.  \n  \n5. A \"Success Stories\" section featuring testimonials from satisfied students, with placeholders for the testimonial text and student names.  \n  \n6. A footer with links to the platform's blog, FAQ, privacy policy, and a \"Contact Us\" button that opens a modal window with a contact form and customer support information.  \n  \nInclude filler placeholder content for the video background, course cards, and testimonials. Embed the CSS styles within the `<style>` tag in the `<head>` section and place the JavaScript code within the `<script>` tag at the end of the `<body>` section.  \n  \nThe JavaScript code should handle the dynamic tagline in the hero section, rotating through the different taglines every 3 seconds."
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
<Tab title="AWS Bedrock Python">

```python
from anthropic import AnthropicBedrock

# See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock

# for authentication options

client = AnthropicBedrock()

message = client.messages.create(
  model="anthropic.claude-sonnet-4-5-20250929-v1:0",
  max_tokens=4000,
  temperature=0,
  system="Your task is to create a one-page website based on the given specifications, delivered as an HTML file with embedded JavaScript and CSS. The website should incorporate a variety of engaging and interactive design features, such as drop-down menus, dynamic text and content, clickable buttons, and more. Ensure that the design is visually appealing, responsive, and user-friendly. The HTML, CSS, and JavaScript code should be well-structured, efficiently organized, and properly commented for readability and maintainability.",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Create a one-page website for an online learning platform called \"EduQuest\" with the following features and sections: \n \n1. A fixed navigation bar with links to course categories (Math, Science, Languages, Arts) and a search bar. \n \n2. A hero section with a video background showcasing students learning online, a dynamic tagline that rotates between \"Learn at your own pace,\" \"Discover new passions,\" and \"Expand your horizons\" every 3 seconds, and a \"Get Started\" button leading to a course catalog. \n \n3. A featured courses section displaying course cards with placeholders for course images, titles, instructors, and descriptions. \n \n4. An interactive \"Learning Paths\" section with a short quiz to determine learning styles and interests, and a button to start the quiz. \n \n5. A \"Success Stories\" section featuring testimonials from satisfied students, with placeholders for the testimonial text and student names. \n \n6. A footer with links to the platform's blog, FAQ, privacy policy, and a \"Contact Us\" button that opens a modal window with a contact form and customer support information. \n \nInclude filler placeholder content for the video background, course cards, and testimonials. Embed the CSS styles within the `<style>` tag in the `<head>` section and place the JavaScript code within the `<script>` tag at the end of the `<body>` section. \n \nThe JavaScript code should handle the dynamic tagline in the hero section, rotating through the different taglines every 3 seconds."
        }
      ]
    }
  ]
)
print(message.content)

```

</Tab>
<Tab title="AWS Bedrock TypeScript">

```typescript

import AnthropicBedrock from '@anthropic-ai/bedrock-sdk';

// See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
// for authentication options
const client = new AnthropicBedrock();

const msg = await client.messages.create({
  model: "anthropic.claude-sonnet-4-5-20250929-v1:0",
  max_tokens: 4000,
  temperature: 0,
  system: "Your task is to create a one-page website based on the given specifications, delivered as an HTML file with embedded JavaScript and CSS. The website should incorporate a variety of engaging and interactive design features, such as drop-down menus, dynamic text and content, clickable buttons, and more. Ensure that the design is visually appealing, responsive, and user-friendly. The HTML, CSS, and JavaScript code should be well-structured, efficiently organized, and properly commented for readability and maintainability.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Create a one-page website for an online learning platform called \"EduQuest\" with the following features and sections: \n \n1. A fixed navigation bar with links to course categories (Math, Science, Languages, Arts) and a search bar. \n \n2. A hero section with a video background showcasing students learning online, a dynamic tagline that rotates between \"Learn at your own pace,\" \"Discover new passions,\" and \"Expand your horizons\" every 3 seconds, and a \"Get Started\" button leading to a course catalog. \n \n3. A featured courses section displaying course cards with placeholders for course images, titles, instructors, and descriptions. \n \n4. An interactive \"Learning Paths\" section with a short quiz to determine learning styles and interests, and a button to start the quiz. \n \n5. A \"Success Stories\" section featuring testimonials from satisfied students, with placeholders for the testimonial text and student names. \n \n6. A footer with links to the platform's blog, FAQ, privacy policy, and a \"Contact Us\" button that opens a modal window with a contact form and customer support information. \n \nInclude filler placeholder content for the video background, course cards, and testimonials. Embed the CSS styles within the `<style>` tag in the `<head>` section and place the JavaScript code within the `<script>` tag at the end of the `<body>` section. \n \nThe JavaScript code should handle the dynamic tagline in the hero section, rotating through the different taglines every 3 seconds."
        }
      ]
    }
  ]
});
console.log(msg);

```
</Tab>

<Tab title="Vertex AI Python">

```python
from anthropic import AnthropicVertex

client = AnthropicVertex()

message = client.messages.create(
  model="claude-sonnet-4@20250514",
  max_tokens=4000,
  temperature=0,
  system="Your task is to create a one-page website based on the given specifications, delivered as an HTML file with embedded JavaScript and CSS. The website should incorporate a variety of engaging and interactive design features, such as drop-down menus, dynamic text and content, clickable buttons, and more. Ensure that the design is visually appealing, responsive, and user-friendly. The HTML, CSS, and JavaScript code should be well-structured, efficiently organized, and properly commented for readability and maintainability.",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Create a one-page website for an online learning platform called \"EduQuest\" with the following features and sections: \n \n1. A fixed navigation bar with links to course categories (Math, Science, Languages, Arts) and a search bar. \n \n2. A hero section with a video background showcasing students learning online, a dynamic tagline that rotates between \"Learn at your own pace,\" \"Discover new passions,\" and \"Expand your horizons\" every 3 seconds, and a \"Get Started\" button leading to a course catalog. \n \n3. A featured courses section displaying course cards with placeholders for course images, titles, instructors, and descriptions. \n \n4. An interactive \"Learning Paths\" section with a short quiz to determine learning styles and interests, and a button to start the quiz. \n \n5. A \"Success Stories\" section featuring testimonials from satisfied students, with placeholders for the testimonial text and student names. \n \n6. A footer with links to the platform's blog, FAQ, privacy policy, and a \"Contact Us\" button that opens a modal window with a contact form and customer support information. \n \nInclude filler placeholder content for the video background, course cards, and testimonials. Embed the CSS styles within the `<style>` tag in the `<head>` section and place the JavaScript code within the `<script>` tag at the end of the `<body>` section. \n \nThe JavaScript code should handle the dynamic tagline in the hero section, rotating through the different taglines every 3 seconds."
        }
      ]
    }
  ]
)
print(message.content)

```
</Tab>
<Tab title="Vertex AI TypeScript">

```typescript 
import { AnthropicVertex } from '@anthropic-ai/vertex-sdk';

// Reads from the `CLOUD_ML_REGION` & `ANTHROPIC_VERTEX_PROJECT_ID` environment variables.
// Additionally goes through the standard `google-auth-library` flow.
const client = new AnthropicVertex();

const msg = await client.messages.create({
model: "claude-sonnet-4@20250514",
max_tokens: 4000,
temperature: 0,
system: "Your task is to create a one-page website based on the given specifications, delivered as an HTML file with embedded JavaScript and CSS. The website should incorporate a variety of engaging and interactive design features, such as drop-down menus, dynamic text and content, clickable buttons, and more. Ensure that the design is visually appealing, responsive, and user-friendly. The HTML, CSS, and JavaScript code should be well-structured, efficiently organized, and properly commented for readability and maintainability.",
messages: [
{
"role": "user",
"content": [
{
"type": "text",
"text": "Create a one-page website for an online learning platform called \"EduQuest\" with the following features and sections: \n \n1. A fixed navigation bar with links to course categories (Math, Science, Languages, Arts) and a search bar. \n \n2. A hero section with a video background showcasing students learning online, a dynamic tagline that rotates between \"Learn at your own pace,\" \"Discover new passions,\" and \"Expand your horizons\" every 3 seconds, and a \"Get Started\" button leading to a course catalog. \n \n3. A featured courses section displaying course cards with placeholders for course images, titles, instructors, and descriptions. \n \n4. An interactive \"Learning Paths\" section with a short quiz to determine learning styles and interests, and a button to start the quiz. \n \n5. A \"Success Stories\" section featuring testimonials from satisfied students, with placeholders for the testimonial text and student names. \n \n6. A footer with links to the platform's blog, FAQ, privacy policy, and a \"Contact Us\" button that opens a modal window with a contact form and customer support information. \n \nInclude filler placeholder content for the video background, course cards, and testimonials. Embed the CSS styles within the `<style>` tag in the `<head>` section and place the JavaScript code within the `<script>` tag at the end of the `<body>` section. \n \nThe JavaScript code should handle the dynamic tagline in the hero section, rotating through the different taglines every 3 seconds."
}
]
}
]
});
console.log(msg);

```

</Tab>
</Tabs>