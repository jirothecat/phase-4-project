// src/components/RecipeList.js
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function RecipeList() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/recipes')
      .then(r => r.json())
      .then(data => {
        setRecipes(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error:', error);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ padding: '2rem' }}>
      <h2>All Recipes</h2>
      <div style={{ display: 'grid', gap: '1rem' }}>
        {recipes.map(recipe => (
          <div key={recipe.id} style={{ border: '1px solid #ddd', padding: '1rem' }}>
            <h3>{recipe.title}</h3>
            <p>{recipe.description}</p>
            <Link to={`/recipes/${recipe.id}`}>View Details</Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecipeList;