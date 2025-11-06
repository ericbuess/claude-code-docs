# Prompt Library

<div id="content-container">
  <div id="prompt-library-container">
    <h1 className="prompt-library-title">Prompt Library</h1>

    <p className="prompt-library-description">
      Explore optimized prompts for a breadth of business and personal tasks.
    </p>
  </div>

  <div className="main-content" id="content-container">
    <div className="prompt-controllers">
      <div className="prompt-search-container">
        <div className="prompt-search-icon-container">
          <svg className="prompt-search-icon" />
        </div>

        <input
          name="search"
          className="prompt-search-bar"
          placeholder="Search..."
          onChange={(e) => {
          window.searchPrompts(e.target.value);
        }}
        />
      </div>

      <div className="relative">
        <div className="dropdown-icon-container">
          <svg className="dropdown-icon" />
        </div>

        <div
          id="category-select"
          onClick={() => {
          window.showDropdown();
        }}
        />

        <div id="categories-dropdown" />

        <div
          id="categories-dropdown-clickout"
          onClick={() => {
          window.hideDropdown();
        }}
        />
      </div>
    </div>

    <div id="prompts-container" />
  </div>
</div>
