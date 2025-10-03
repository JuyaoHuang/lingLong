import { GetIndexFromSlugID } from "./hash";
import LingLongConfig from "../../linglong.config";

/**
 * Retrieves the cover URL for an unspecified entry based on the provided ID.
 * 根据提供的 ID 检索未指定条目的封面 URL。
 * @param id - The unique identifier for the entry.
 * @returns The URL of the corresponding cover image.
 */
export function GetCoverURLForUnspecifiedEntry(id: string): string {
  const index = GetIndexFromSlugID(id, LingLongConfig.banners.length);
  return LingLongConfig.banners[index];
}
