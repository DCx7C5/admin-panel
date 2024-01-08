import { useEffect } from 'react';
import PropTypes from 'prop-types';

function useCopyStyles(source, target = null) {
  useEffect(() => {
    const sourceElement = source && source.current;

    if (!sourceElement || !(sourceElement instanceof Element)) return;

    if (target) {
      let targetElement;

      if (target.hasOwnProperty('current') && target.current instanceof Element) {
        // If target is an element ref
        targetElement = target.current;
      } else if (target instanceof Element) {
        // If target is an element
        targetElement = target;
      } else if (target.nodeType === 1) {
        // If target is a node
        targetElement = target;
      } else {
        return; // Invalid target type
      }

      const sourceStyles = window.getComputedStyle(sourceElement);

      for (const property of sourceStyles) {
        targetElement.style[property] = sourceStyles.getPropertyValue(property);
      }

      targetElement.setAttribute('style', sourceElement.getAttribute('style'));
    }
  }, [source, target]);

  if (!target) {
    const sourceElement = source && source.current;

    if (!sourceElement || !(sourceElement instanceof Element)) return null;

    const sourceStyles = window.getComputedStyle(sourceElement);
    const styles = {};

    for (const property of sourceStyles) {
      styles[property] = sourceStyles.getPropertyValue(property);
    }

    return styles;
  }

  return null;
}

useCopyStyles.propTypes = {
  source: PropTypes.oneOfType([
    PropTypes.shape({ current: PropTypes.instanceOf(Element) }),
    PropTypes.instanceOf(Element),
    PropTypes.object,
  ]),
  target: PropTypes.oneOfType([
    PropTypes.shape({ current: PropTypes.instanceOf(Element) }),
    PropTypes.instanceOf(Element),
    PropTypes.object,
  ]),
};

export default useCopyStyles;
