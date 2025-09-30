import { toString as mdastToString } from "mdast-util-to-string";
import getReadingTime from "reading-time";

export function remarkReadingTime() {
  return (tree, { data }) => {
    const textOnPage = mdastToString(tree);
    const readingTime = getReadingTime(textOnPage);
    data.astro.frontmatter.readingMetadata = {
      time: Math.max(1, Math.round(readingTime.minutes)),
      wordCount: readingTime.words,
    };
  };
}
