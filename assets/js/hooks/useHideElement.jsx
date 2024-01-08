import {useState} from "react";
import {useLocalStorage} from "./useStorage";
import PropTypes from "prop-types";


export const useHideElement = (initialValue = false, storageKey = null) => {
  const [isVisible, setIsVisible, _] = (typeof storageKey === 'string')
    ? useLocalStorage(storageKey, initialValue)
    : useState(initialValue)

  const hide = () => {
    setIsVisible(false)
  }

  const show = () => {
    setIsVisible(true)
  }

  const toggle = () => {
    setIsVisible((prev) => !prev)
  }

  return [
    isVisible,
    hide,
    show,
    toggle
  ]
}

useHideElement.propTypes = {
  initialValue: PropTypes.bool.isRequired,
  storageKey: PropTypes.string
}


export default useHideElement