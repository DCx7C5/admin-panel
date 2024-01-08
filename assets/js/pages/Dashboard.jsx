import ReactDOM from "react-dom/client";
import React, {StrictMode} from "react";
import RealTimeClock from "../components/Clock";
import {DevSupport} from "@react-buddy/ide-toolbox";
import {ComponentPreviews, useInitial} from "../dev";
import Base from "../Base";



const DashBoard = () => {
  return (
    <StrictMode>
      <DevSupport ComponentPreviews={ComponentPreviews} useInitialHook={useInitial}>
      <div id='dashboard'>
        <RealTimeClock/>
      </div>
      </DevSupport>
    </StrictMode>
  )
}


ReactDOM.createRoot(document.getElementById('content-wrapper')).render(
  <Base>
    <DashBoard />
  </Base>
)