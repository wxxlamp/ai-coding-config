#!/usr/bin/env node
/**
 * HTML to Markdown Converter for Yuque Documents
 * This script converts HTML content from Yuque pages to Markdown format
 */

function htmlToMarkdown(element) {
  let markdown = '';

  for (const node of element.childNodes) {
    if (node.nodeType === Node.TEXT_NODE) {
      markdown += node.textContent;
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      const tag = node.tagName.toLowerCase();
      const content = htmlToMarkdown(node);

      switch (tag) {
        case 'h1':
          markdown += `# ${content.trim()}\n\n`;
          break;
        case 'h2':
          markdown += `## ${content.trim()}\n\n`;
          break;
        case 'h3':
          markdown += `### ${content.trim()}\n\n`;
          break;
        case 'h4':
          markdown += `#### ${content.trim()}\n\n`;
          break;
        case 'h5':
          markdown += `##### ${content.trim()}\n\n`;
          break;
        case 'h6':
          markdown += `###### ${content.trim()}\n\n`;
          break;
        case 'p':
          markdown += `${content.trim()}\n\n`;
          break;
        case 'br':
          markdown += '\n';
          break;
        case 'strong':
        case 'b':
          markdown += `**${content}**`;
          break;
        case 'em':
        case 'i':
          markdown += `*${content}*`;
          break;
        case 'code':
          markdown += `\`${content}\``;
          break;
        case 'pre':
          markdown += `\`\`\`\n${content.trim()}\n\`\`\`\n\n`;
          break;
        case 'blockquote':
          markdown += `> ${content.trim().replace(/\n/g, '\n> ')}\n\n`;
          break;
        case 'a':
          const href = node.getAttribute('href') || '';
          markdown += `[${content}](${href})`;
          break;
        case 'img':
          const src = node.getAttribute('src') || '';
          const alt = node.getAttribute('alt') || '';
          markdown += `![${alt}](${src})\n\n`;
          break;
        case 'ul':
          const ulItems = Array.from(node.children)
            .filter(child => child.tagName.toLowerCase() === 'li')
            .map(li => `- ${htmlToMarkdown(li).trim()}`)
            .join('\n');
          markdown += `${ulItems}\n\n`;
          break;
        case 'ol':
          const olItems = Array.from(node.children)
            .filter(child => child.tagName.toLowerCase() === 'li')
            .map((li, i) => `${i + 1}. ${htmlToMarkdown(li).trim()}`)
            .join('\n');
          markdown += `${olItems}\n\n`;
          break;
        case 'li':
          if (node.parentElement &&
              node.parentElement.tagName.toLowerCase() !== 'ul' &&
              node.parentElement.tagName.toLowerCase() !== 'ol') {
            markdown += content;
          } else {
            markdown += content;
          }
          break;
        case 'div':
        case 'span':
        case 'section':
        case 'article':
        default:
          markdown += content;
      }
    }
  }

  return markdown;
}

// Export for use in browser context or Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { htmlToMarkdown };
}

// Browser global
if (typeof window !== 'undefined') {
  window.YuqueHtmlToMarkdown = { htmlToMarkdown };
}
