import { createContext, useState } from "react";

const FetchContext = createContext({});

// eslint-disable-next-line react/prop-types
export const FetchContextProvider = ({ children }) => {
  const [selectedButton, setSelectedButton] = useState("select");
  const [articlesData, setArticlesData] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchArticles = async (page, size) => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/articles/?page=${page}&size=${size}`,
        { credentials: "include" }
      );

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();
      setArticlesData(data);
      console.log(data);
      setLoading(false);
    } catch (error) {
      console.error("Error:", error);
      setLoading(false);
    }
  };

  const searchArticles = async (searchTerm, page, size) => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/articles/search/${searchTerm}?page=${page}&size=${size}`,
        { credentials: "include" }
      );

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();
      setArticlesData(data);
      console.log(data);
      setLoading(false);
    } catch (error) {
      console.error("Error:", error);
      setLoading(false);
    }
  };

  const context = {
    articlesData,
    selectedButton,
    setSelectedButton,
    searchArticles,
    fetchArticles,
    loading,
  };

  return (
    <FetchContext.Provider value={context}>{children}</FetchContext.Provider>
  );
};

export default FetchContext;
