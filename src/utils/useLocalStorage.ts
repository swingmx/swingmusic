/**
 * Retrieeves the value of a key from localStorage.
 * @param key the key to read from local storage
 * @returns A javascript object representing the value stored in local storage
 */
export function readLocalStorage(key: string) {
  return JSON.parse(localStorage.getItem(key));
}

/**
 * Stores a value in localStorage.
 * @param key the key to store the value in local storage
 * @param value the value to store in local storage
 * @returns true if the value was successfully stored, false otherwise
 * @throws if the value is not a valid JSON string
 */

export function writeLocalStorage(key: string, value: any) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch (e) {
    return false;
  }
}
