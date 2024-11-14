import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from "./Navbar";
import Home from "./Home";
import RecipeList from "./RecipeList";
import CreateRecipe from "./CreateRecipe";
import RecipeDetail from "./RecipeDetail";

function App() {
  return (
    <Router>
      <div>
        <NavBar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/recipes" element={<RecipeList />} />
          <Route path="/recipes/new" element={<CreateRecipe />} />
          <Route path="/recipes/:id" element={<RecipeDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;