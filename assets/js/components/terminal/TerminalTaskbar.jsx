import React from "react";
import PropTypes from "prop-types";


const TerminalTaskbar = ({position, children}) => {


  return (
    <div className={'term-taskbar term-taskbar-'+position} >
      {children && children.map((value, index) =>
        <div key={index}>{value}</div>
      )}
    </div>
  )
}

export default TerminalTaskbar