import React, { createContext, useContext, useEffect, useState } from "react";

export const DataContext = createContext(null);

export const useData = () => {
  return useContext(DataContext);
};

export const DataProvider = ({ dataElementId, children }) => {
  const [data, setData] = useState(() => parseUserData());

  useEffect(() => {
    if (data === null) {
      setData(parseUserData());
    }
  }, [data]);

  function parseUserData() {
    const elem = document.getElementById(dataElementId);
    if (elem) {
      const data = JSON.parse(elem.textContent);
      return data || {}
    }
    return {};
  }

  return (
    <DataContext.Provider value={data}>
      {children}
    </DataContext.Provider>
  );
};

export default DataProvider;
