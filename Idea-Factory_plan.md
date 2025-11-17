

* * *

### **Updated Instructions for Claude Code**

#### **1. Define the App’s Core Purpose**

**Prompt to Claude:**

``Build a fully functional, mobile-compatible web app called "Idea Factory" based on the following core purpose and principles: ### Core Purpose: - Generate **novel, cross-disciplinary ideas** based on user input. - Refine ideas into **actionable plans**. - Output results in a **polished, mobile-friendly format**.  ### Key Principles: - The app should be **self-contained** (only use Claude API as an external dependency). - Prioritize **simplicity, speed, and mobile compatibility**. - Use a **minimalist UI/UX** that is clean and intuitive.  ### Requirements: 1. **Frontend:**    - Use **Streamlit** for a simple, mobile-friendly UI.    - Include the following screens:      - **Home:** Input field for topics + "Generate Ideas" button.      - **Results:** Display generated ideas as bullet points.      - **Refinement:** Option to refine a selected idea into a step-by-step plan.      - **Visualization:** Show refined ideas as a mind map or structured report.  2. **Backend:**    - Use **Python with FastAPI** to handle API calls to Claude.    - Implement the following endpoints:      - `/generate`: Accepts user input, returns 10 novel ideas.      - `/refine`: Accepts a selected idea, returns a step-by-step plan.      - `/visualize`: Accepts a list of ideas, returns a Mermaid.js mind map or report.  3. **Deployment:**    - Deploy the frontend on **Streamlit Sharing**.    - Deploy the backend on **Render** (free tier).    - Ensure the app is fully functional on mobile browsers.  ### Constraints: - Use only **Python, Streamlit, FastAPI, and Claude API**. - Optimize for **speed and minimalism**. - No external databases (use local storage or session state).  ### Deliverables: 1. A **GitHub repository** with the full codebase. 2. A **live demo link** for testing. 3. Instructions for how to run and extend the app.  Proceed step-by-step, asking for clarification if needed. Start by outlining the project structure and dependencies.``

* * *

#### **2. Implement Core Features**

**Prompt to Claude:**

`Implement the core features of the Idea Factory app based on the following guidelines: ### Core Features: 1. **Idea Generation:**    - When the user inputs a topic (e.g., "quantum physics + storytelling"), generate **10 novel, actionable ideas**.    - Format each idea as a concise bullet point.    - Use this template for Claude's prompt:      ```      Generate 10 creative, actionable ideas combining [user_input]. Each idea should be unique, specific, and formatted as a bullet point. Avoid generic suggestions.      ```  2. **Idea Refinement:**    - When the user selects an idea, refine it into a **step-by-step plan** with tasks, challenges, and resources.    - Use this template for Claude's prompt:      ```      Refine the following idea into a detailed plan: "[selected_idea]".      Output a markdown table with columns: Task | Challenges | Resources.      Include 3-5 tasks, 2-3 challenges, and specific resources/tools.      ```  3. **Visualization:**    - When the user requests visualization, format the ideas or plans into a **Mermaid.js mind map** or structured report.    - Use this template for Claude's prompt:      ```      Format the following ideas into a Mermaid.js mind map:      [list_of_ideas]      Root node: [user_input]      Example:      ```mermaid      mindmap        root((Quantum Physics + Storytelling))          YouTube Series            Interactive Sci-Fi Stories          Board Game            Quantum Puzzle Mechanics      ```      ```  ### Constraints: - Ensure all features work seamlessly on mobile. - Use **session state in Streamlit** to pass data between screens. - Optimize Claude API calls for speed (limit tokens, use clear prompts).  Proceed by implementing these features one by one. Start with **Idea Generation**.`

* * *

#### **3. Optimize for Mobile and Polish**

**Prompt to Claude:**

`Optimize the Idea Factory app for mobile use and polish the UI/UX based on the following guidelines: ### Mobile Optimization: 1. **Layout:**    - Use Streamlit's layout features to ensure buttons and text are large and tappable.    - Test on mobile browsers (Chrome/Safari) for responsiveness.  2. **Performance:**    - Cache Claude API responses to avoid redundant calls.    - Use loading spinners for API calls.  3. **Offline Support:**    - Store generated ideas in session state so users can revisit them.  ### Polish: 1. **UI:**    - Add a clean header with the app name and a brief description.    - Use consistent fonts/colors (e.g., dark mode for readability).  2. **Error Handling:**    - Guide users to rephrase inputs if Claude's output is off-topic.    - Add retries for failed API calls.  3. **Sharing:**    - Allow users to export ideas/plans as text or images.  ### Deliverables: 1. A fully **mobile-optimized app**. 2. A **polished UI** with no clutter. 3. Instructions for users on how to get the most out of the app.  Proceed by implementing these optimizations. Start with **mobile layout adjustments**.`

* * *


