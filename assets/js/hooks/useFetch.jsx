import useAsync from "./useAsync";
import PropTypes from "prop-types";


const DEFAULT_OPTIONS = {
  headers: { "Content-Type": "application/json" },
}

export const useFetch = (url, options = {}, dependencies = []) => {
  return useAsync(() => {
    return fetch(url, { ...DEFAULT_OPTIONS, ...options }).then(res => {
      if (res.ok) return res.json()
      return res.json().then(json => Promise.reject(json))
    })
  }, dependencies)
}

useFetch.propTypes = {
  url: PropTypes.string.isRequired,
  options: PropTypes.object,
  dependencies: PropTypes.arrayOf(PropTypes.any),
};


export default useFetch