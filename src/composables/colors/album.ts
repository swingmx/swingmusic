/**
 * Returns `true` if the rgb color passed is light.
 *
 * @param {string} rgb The color to check whether it's light or dark.
 * @returns {boolean} true if color is light, false if color is dark.
 */
export function isLight(rgb: string): boolean {
  if (rgb == null || undefined) return false;

  const [r, g, b] = rgb.match(/\d+/g)!.map(Number);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;

  return brightness > 165;
}

interface BtnColor {
  color: string;
  isDark: boolean;
}

/**
 * Returns the luminance of a color.
 * @param r The red value of the color.
 * @param g The green value of the color.
 * @param b The blue value of the color.
 */
export function luminance(r: any, g: any, b: any) {
  let a = [r, g, b].map(function (v) {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
}

/**
 * Returns a contrast ratio of `color1`:`color2`
 * @param {string} color1 The first color
 * @param {string} color2 The second color
 */
export function contrast(color1: number[], color2: number[]): number {
  let lum1 = luminance(color1[0], color1[1], color1[2]);
  let lum2 = luminance(color2[0], color2[1], color2[2]);
  let brightest = Math.max(lum1, lum2);
  let darkest = Math.min(lum1, lum2);
  return (brightest + 0.05) / (darkest + 0.05);
}

/**
 * Converts a rgb color string to an array of the form: `[r, g, b]`
 * @param rgb The color to convert
 * @returns {number[]} The array representation of the color
 */
export function rgbToArray(rgb: string): number[] {
  return rgb.match(/\d+/g)!.map(Number);
}

/**
 * Returns true if the `color2` contrast with `color1`.
 * @param color1 The first color
 * @param color2 The second color
 */
export function theyContrast(color1: string, color2: string) {
  return contrast(rgbToArray(color1), rgbToArray(color2)) > 3;
}
