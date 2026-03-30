import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: "AIzaSyCbvMZBeRMYwctch6lXUlaxHd168IAJlAU"});

async function main(){
    const response = await ai.models.generateContent({
        model: "gemini-3.1-flash-lite-preview",
        contents: "What is deep learning",
    });
    console.log(response.text);
}

main();