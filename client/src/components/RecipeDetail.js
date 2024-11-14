// src/components/RecipeDetail.js
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function RecipeDetail() {
  const { id } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/recipes/${id}`)
      .then(r => r.json())
      .then(data => {
        setRecipe(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error:', error);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (!recipe) return <div>Recipe not found</div>;

  return (
    <div style={{ padding: '2rem' }}>
      <h2>{recipe.title}</h2>
      <p>{recipe.description}</p>
      <div>
        <h3>Instructions:</h3>
        <p>{recipe.instructions}</p>
      </div>
      <div>
        <h3>Cooking Time:</h3>
        <p>{recipe.cooking_time} minutes</p>
      </div>
    </div>
  );
}

export default RecipeDetail;