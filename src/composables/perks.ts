import { RouteLocationNormalized } from "vue-router";

function getElem(id: string, type: string) {
  switch (type) {
    case "class": {
      return document.getElementsByClassName(id)[0];
    }
    case "id": {
      return document.getElementById(id);
    }
  }
}

type r = RouteLocationNormalized;

function isSameRoute(to: r, from: r) {
  if (to.params.path == from.params.path) {
    return true;
  }

  return false;
}

export { getElem, isSameRoute };
