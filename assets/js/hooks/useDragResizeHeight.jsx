import {useEffect, useRef, useState} from "react";
import useEventListener from "./useEventListener";
import {useLocalStorage} from "./useStorage";


const useDragResizeHeight = (resizable, callbackFunc = null) => {
  const [isDown, setIsDown] = useState(false);
  const [lastHeightStorage, setLastHeightStorage] = useLocalStorage('term.height', 0);
  const [height, setHeight] = useState(lastHeightStorage);
  const lastY = useRef(0);

  useEffect(() => {
    setHeight(lastHeightStorage)
  }, []);


  const handleMouseMove = e => {
    e.preventDefault();
    const realHeight = resizable.current.style.height
    const viewPortHeight = window.innerHeight
    if (isDown && resizable.current) {
      callbackFunc && callbackFunc()
      const deltaY = viewPortHeight - e.y;
      if (deltaY < 0 && (parseInt(realHeight) === 0)) {
        setHeight(0)
        lastY.current = 0
      } else {
        setHeight(deltaY)
        lastY.current = deltaY
      }
    }
  }

  useEventListener('mousemove', handleMouseMove)

  const onMouseDown = e => {
    setIsDown(true);
    e.preventDefault();
    resizable.current.style.cursor = 'row-resize'
    window.addEventListener('mouseup', handleMouseUp)
  }

  const handleMouseUp = e => {
    e.preventDefault()
    setIsDown(false)
    setLastHeightStorage(lastY.current)
    resizable.current.style.cursor = null
    window.removeEventListener('mouseup', handleMouseUp)
  }


  return {height, onMouseDown, setHeight, lastHeightStorage, setLastHeightStorage}
}

export default useDragResizeHeight