import express, { Express, Request, Response } from "express";
import cors from "cors";

const app: Express = express();

app.use(express.json());
app.use(cors());
app.use(express.static("public"));

type URLParams = null;
type RequestBody = { ingredients: string[]; cuisine: string };
type ResponseBody = { recipe: string; instructions: string; mealDescription: string };

app.post(
  "/api/generateRecipe",
  async (req: Request<URLParams, ResponseBody, RequestBody>, res: Response) => {
    const { ingredients, cuisine } = req.body;
    const recipe = `Recipe for ${cuisine} using ${ingredients.join(", ")}`;
    const instructions = `Cook the ${recipe} by doing X, Y, and Z.`;
    const mealDescription = `Enjoy a delicious meal of ${recipe} with your family and friends.`;
    res.status(200).json({ recipe, instructions, mealDescription });
  }
);

app.listen(3000, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:3000`);
});