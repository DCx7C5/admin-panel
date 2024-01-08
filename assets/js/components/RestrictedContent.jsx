import React, {Suspense} from "react";
import {useData} from "./DataProvider";


export const RestrictedContent = ({ children }) => {
  const { is_superuser } = useData();

  return (
    <>
      <Suspense>
        {is_superuser && children}
      </Suspense>
    </>
  )
}


