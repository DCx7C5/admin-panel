import ReactDOM from "react-dom/client";
import Base from "./pages/Base";
import React, {StrictMode} from "react";
import DashBoard from "./pages/Dashboard";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import NoMatch from "./pages/NoMatch";
import {ComponentPreviews, useInitial} from "./dev";
import {DevSupport} from "@react-buddy/ide-toolbox";


ReactDOM.createRoot(document.getElementById('content-wrapper')).render(
    <Base>
        <StrictMode>
            <DevSupport ComponentPreviews={ComponentPreviews} useInitialHook={useInitial}>
                <BrowserRouter>
                    <Routes>
                        <Route path="/">
                            <Route index element={<DashBoard />} />
                            <Route path="*" element={<NoMatch />} />
                        </Route>
                    </Routes>
                </BrowserRouter>
            </DevSupport>
        </StrictMode>
    </Base>
)