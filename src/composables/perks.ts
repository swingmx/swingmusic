const putCommas = (artists: string[]) => {
  let result = [];

  artists.forEach((i, index, artists) => {
    if (index !== artists.length - 1) {
      result.push(i + ", ");
    } else {
      result.push(i);
    }
  });

  return result;
};

function focusElem(className: string, delay?: number) {
  const dom = document.getElementsByClassName(className)[0];

  setTimeout(() => {
    if (dom) {
      dom.scrollIntoView({
        behavior: "smooth",
        block: "start",
        inline: "center",
      });
    }
  }, delay | 300);
}

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

/**
 * Converts seconds into minutes and hours.
 * @param seconds The seconds to convert
 * @param long Whether to provide the time in the long format
 */
function formatSeconds(seconds: number, long?: boolean) {
  const date = new Date(seconds * 1000);

  const hh = date.getUTCHours();
  const mm = date.getUTCMinutes();
  const ss = date.getUTCSeconds();

  let _hh = hh < 10 ? `0${hh}` : hh;
  let _mm = mm < 10 ? `0${mm}` : mm;
  let _ss = ss < 10 ? `0${ss}` : ss;

  if (long == true) {
    if (hh === 1) {
      _hh = hh + " Hour";
    } else {
      _hh = `${hh} Hours`;
    }

    if (mm === 1) {
      _mm = mm + " Minute";
    } else {
      _mm = `${mm} Minutes`;
    }

    if (hh > 0) {
      return `${_hh}, ${_mm}`;
    } else {
      return `${_mm}`;
    }
  }

  if (hh > 0) {
    return `${_hh}:${_mm}:${_ss}`;
  } else {
    return `${_mm}:${_ss}`;
  }
}

export { putCommas, focusElem, formatSeconds, getElem };
