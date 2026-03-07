---
name: yuque-doc-downloader
description: Download Yuque documents to local markdown files using browser automation. Use when you need to export a Yuque document to a local markdown file.
---

# Yuque Doc Downloader

Download a Yuque document to a local markdown file using browser automation.

## Usage

```
skill: "yuque-doc-downloader", args: "<yuque-doc-url> [<output-path>]"
```

## Arguments

- `yuque-doc-url` (required): The full URL of the Yuque document to download. Supports:
  - Standard Yuque: `https://www.yuque.com/username/repo/slug`
  - Ali Internal Yuque: `https://yuque.alibaba-inc.com/namespace/doc_slug`
  - Antfin Yuque: `https://aliyuque.antfin.com/namespace/doc_slug`
- `output-path` (optional): The local file path to save the markdown file. Defaults to the document slug name with `.md` extension.

---

When invoked, perform the following actions to download the Yuque document:

### Step 1: Parse the Input URL

1.1. Extract the document slug from the provided URL path.

1.2. Identify the supported domain type:
   - Standard Yuque: `https://www.yuque.com/`
   - Ali Internal Yuque: `https://yuque.alibaba-inc.com/`
   - Antfin Yuque: `https://aliyuque.antfin.com/`

1.3. Parse the path segments to determine:
   - Namespace (format: `{group_or_user}/{repo}` or `{repo}` for personal docs)
   - Document slug (the last segment of the URL path)

### Step 2: Navigate to the Document Page

2.1. Use the `puppeteer_navigate` tool to navigate to the provided Yuque URL.

2.2. Wait for the page to fully load (allow 2-3 seconds for dynamic content).

### Step 3: Extract Document Metadata

3.1. Execute JavaScript to extract the document title:
   - Query for `h1[data-testid="doc-title"]` or the first `h1` element
   - If not found, extract from `document.title`

3.2. Identify the main content container:
   - Try selectors in order: `[data-testid="lake-content"]`, `.lake-content`, `.ne-doc-content`, `article`, `[class*="content"]`
   - Select the first container with substantial content (>500 characters)

### Step 4: Convert Content to Markdown

4.1. Traverse the DOM tree of the content container recursively.

4.2. Convert each element to corresponding Markdown syntax:
   - Headings (`h1`-`h6`): Convert to `#` - `######`
   - Paragraphs (`p`): Preserve as plain text with line breaks
   - Bold (`strong`, `b`): Wrap with `**`
   - Italic (`em`, `i`): Wrap with `*`
   - Inline code (`code`): Wrap with backticks
   - Code blocks (`pre`): Wrap with triple backticks
   - Links (`a`): Convert to `[text](url)` format
   - Images (`img`): Convert to `![alt](src)` format
   - Unordered lists (`ul` > `li`): Prefix with `- `
   - Ordered lists (`ol` > `li`): Prefix with `1. `, `2. `, etc.
   - Blockquotes (`blockquote`): Prefix with `> `

4.3. Clean up the generated Markdown:
   - Remove excessive line breaks
   - Trim whitespace
   - Preserve image URLs as-is

### Step 5: Save to Local File

5.1. Determine the output filename:
   - If `output-path` is provided, use it
   - Otherwise, use the document slug with `.md` extension

5.2. Write the Markdown content to the file using the `Write` tool.

5.3. Include the document title as the first-level heading (`# Title`).

### Step 6: Report Results

6.1. Confirm successful download with the following information:
   - Document title
   - Source URL
   - Output file path
   - Approximate content length (character count)

6.2. If any errors occur during the process, report:
   - The specific step where the error occurred
   - The error message
   - Suggestions for troubleshooting

## Examples

### Example 1: Standard Yuque
```
skill: "yuque-doc-downloader", args: "https://www.yuque.com/myname/notes/hello-world ./docs/hello.md"
```

### Example 2: Ali Internal Yuque
```
skill: "yuque-doc-downloader", args: "https://yuque.alibaba-inc.com/myname/notes/hello-world ./docs/hello.md"
```

### Example 3: Antfin Yuque
```
skill: "yuque-doc-downloader", args: "https://aliyuque.antfin.com/chenkai.wsb/ba78e6/frlquena64c3qhvg ./docs/my-doc.md"
```

## Notes

- This skill uses browser automation (Puppeteer) to access documents, which requires the document to be accessible in the browser session.
- Image URLs in the generated Markdown may be internal network addresses that require specific network access to view.
- The conversion from HTML to Markdown is a best-effort process and may not perfectly preserve all formatting.
- For documents with complex layouts or interactive elements, some content may not be captured accurately.
