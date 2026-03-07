---
name: yuque-doc-downloader
description: Download Yuque documents to local markdown files using browser automation, with automatic image upload to cloud storage. Use when you need to export a Yuque document to a local markdown file.
---

# Yuque Doc Downloader

Download a Yuque document to a local markdown file using browser automation. Automatically detects and uploads images to cloud storage, replacing internal URLs with public CDN links.

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

### Step 3: Extract Document Metadata and Images

3.1. Execute JavaScript to extract the document title:
   - Query for `h1[data-testid="doc-title"]` or the first `h1` element
   - If not found, extract from `document.title`

3.2. Identify the main content container:
   - Try selectors in order: `[data-testid="lake-content"]`, `.lake-content`, `.ne-doc-content`, `article`, `[class*="content"]`
   - Select the first container with substantial content (>500 characters)

3.3. Collect all image URLs from the content:
   - Query for all `img` elements within the content container
   - Extract the `src` attribute from each image
   - Filter out empty or invalid URLs
   - Store the mapping of original URLs for later replacement

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
   - Images (`img`): Convert to `![alt](src)` format (using original src for now)
   - Unordered lists (`ul` > `li`): Prefix with `- `
   - Ordered lists (`ol` > `li`): Prefix with `1. `, `2. `, etc.
   - Blockquotes (`blockquote`): Prefix with `> `

4.3. Clean up the generated Markdown:
   - Remove excessive line breaks
   - Trim whitespace
   - Preserve image URLs as-is (will be replaced in Step 6)

### Step 5: Upload Images to Cloud Storage

5.1. Check if any images were found in Step 3.3:
   - If no images, skip to Step 6
   - If images found, proceed with upload process

5.2. For each image URL collected:
   - Use `puppeteer_evaluate` to fetch the image as base64 or blob data
   - Alternatively, download the image temporarily using browser capabilities

5.3. Upload images using the `img-uploader` skill:
   - Invoke `skill: "img-uploader"` with the image data or local path
   - Supported providers: Imgur (recommended), sm.ms, GitHub + jsDelivr CDN
   - Collect the returned public URL for each uploaded image

5.4. Build an image URL mapping table:
   - Map each original internal URL to its corresponding public CDN URL
   - Handle upload failures gracefully (keep original URL if upload fails)

### Step 6: Update Markdown with Public Image URLs

6.1. Review the generated Markdown content from Step 4.

6.2. Replace image URLs using the mapping from Step 5:
   - Find all Markdown image syntax: `![alt](url)`
   - Replace the `url` portion if it exists in the mapping table
   - Preserve the alt text unchanged

6.3. Perform additional URL cleanup:
   - Remove any query parameters that are no longer needed
   - Ensure URLs are properly encoded

### Step 7: Save to Local File

7.1. Determine the output filename:
   - If `output-path` is provided, use it
   - Otherwise, use the document slug with `.md` extension

7.2. Write the Markdown content to the file using the `Write` tool.

7.3. Include the document title as the first-level heading (`# Title`).

### Step 8: Report Results

8.1. Confirm successful download with the following information:
   - Document title
   - Source URL
   - Output file path
   - Approximate content length (character count)
   - Number of images processed and uploaded
   - List of uploaded image URLs (if any)

8.2. If any errors occur during the process, report:
   - The specific step where the error occurred
   - The error message
   - Which images failed to upload (if applicable)
   - Suggestions for troubleshooting

## Examples

### Example 1: Standard Yuque
```
skill: "yuque-doc-downloader", args: "https://www.yuque.com/myname/notes/hello-world ./docs/hello.md"
```

### Example 2: Ali Internal Yuque with Images
```
skill: "yuque-doc-downloader", args: "https://yuque.alibaba-inc.com/myname/notes/hello-world ./docs/hello.md"
```
Images will be automatically uploaded to cloud storage and URLs updated.

### Example 3: Antfin Yuque
```
skill: "yuque-doc-downloader", args: "https://aliyuque.antfin.com/chenkai.wsb/ba78e6/frlquena64c3qhvg ./docs/my-doc.md"
```

## Notes

- This skill uses browser automation (Puppeteer) to access documents, which requires the document to be accessible in the browser session.
- Image upload depends on the `img-uploader` skill being available and configured.
- Uploaded images are stored on public CDNs (Imgur by default) and will be publicly accessible.
- The conversion from HTML to Markdown is a best-effort process and may not perfectly preserve all formatting.
- For documents with complex layouts or interactive elements, some content may not be captured accurately.
- If image upload fails, the original internal URLs will be preserved in the markdown.
