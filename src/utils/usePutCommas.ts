/**
 * Turns a list of artists into a string of artists separated by commas.
 * @param artists artists array to put commas in
 * @returns a string with commas in between each artist
 */
export default (artists: string[]) => {
  const result: string[] = [];

  artists.forEach((i, index, artists) => {
    if (index !== artists.length - 1) {
      result.push(i + ", ");
    } else {
      result.push(i);
    }
  });

  return result;
};
