export function readLocalStorage(key: string) {
  return JSON.parse(localStorage.getItem(key));
}
