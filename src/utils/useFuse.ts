import { useFuse } from "@vueuse/integrations/useFuse";

/**
 * Fuzzy search using Fuse.js
 * @param query The query to search for
 * @param data The list to search in
 * @param fuseOptions Fuse.js options
 * @returns A ref containing the search results
 */
export default (query: string, data: any[], fuseOptions: object) => {
  const { results } = useFuse(query, data, {
    matchAllWhenSearchEmpty: true,
    fuseOptions: { ...fuseOptions, threshold: 0.3, ignoreLocation: true },
  });

  return results;
};
