# Flood Finder
## Preview Images
<img src="https://github.com/Iemontine/FloodFinder/assets/95956143/ee2bac99-6f3d-4940-8d3c-160d9465e137" alt="preview of homepage" width="200"/>
<img src="https://github.com/Iemontine/FloodFinder/assets/95956143/9778324f-c0e4-4147-8f59-a27d36127a45" alt="interaction page" width="200"/>
<img src="https://github.com/Iemontine/FloodFinder/assets/95956143/a90501a1-43b0-42b1-98ff-b42334c68b95" alt="interaction page failure" width="200"/>
<img src="https://github.com/Iemontine/FloodFinder/assets/95956143/b076465b-11ae-443d-a8ef-abcde763c52b" alt="example AI generated response" width="200"/>
<img src="https://github.com/Iemontine/FloodFinder/assets/95956143/1f55b86b-244a-4bc5-a18b-b7c322c74e96" alt="UX/UI design" width="200"/>

## Inspiration
Based on the prompt of "create for social good_", we wanted to build something around the idea of a disaster (flood) detection system and disaster safety recommendation system all in one place. We started developing it to work specifically on floods but did see the opportunity for integrating more types of disaster warnings in the future.

## What it does
We converged on this idea of giving it the capability to detect nearby danger warnings or signs of a flood, then relay a response recommendation using AI generated text. We also wanted to display an embedded map of the nearest flood point to the user to help them gauge their reaction to it. Flood prediction was not implemented, but the LLM integration was.

## How we built it
The frontend uses pure HTML, CSS, JS, and used created a custom Python Flask API that used the OpenAI Function-Calling API to implement Retrieval-Augmented Generation system that ensures the coordinates of the given city are accurate, which is then passed to the Google Earth Engine to obtain flood data. The flood data **would have been** displayed in a user-friendly manner via the embedded map and AI-generated disaster-response recommendation.

## Learning Experiences/Reflection
* I lack knowledge on how or where to host a Flask API, the backbone of being able to host the site online
* Better foresight for how each part of the project will connect (or project scale in general) would have been benefitial
  * We planned on using Google Earth Engine (GEE) to obtain data to train in a machine learning algorithm, but diverged from that idea due to time constraints.
  * Despite these developments, a huge mistake we made was not additionally diverging from the overall project.
  * In other words, we realized too late that GEE obtains data in 6 days.
  * Thereby, users will never be truly warned about nearby floods, merely reported on what GEE had to give.
  * Focusing more on the implementation rather than on web design or dropping the project idea early on, may have permitted this

## Credits
* OpenAI API integration and prompt engineering, web design - Iemontine
* GEE API integration, project idea - acyeow
* html/css implementation - Roro1083
