import { subPath } from "@/interfaces";

/**
 * Breaks a path into sub-paths.
 * @param {string} paths to break into subpaths
 * @returns {subPath[]} an array of subpaths
 */
export default function createSubPaths(paths: string | string[]): subPath[] {
  const pathlist = (paths as string).split("/");
  pathlist.shift();

  const subPaths = pathlist.map((path, index) => {
    return { name: path, path: pathlist.slice(0, index + 1).join("/") };
  });

  return subPaths;
}
