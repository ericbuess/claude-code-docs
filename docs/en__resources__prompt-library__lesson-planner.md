# Lesson planner

Craft in depth lesson plans on any subject.

---

> Copy this prompt into our developer [Console](/login?selectAccount=true&returnTo=%2Fdashboard%3F) to try it for yourself!

|        | Content                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System | Your task is to create a comprehensive, engaging, and well-structured lesson plan on the given subject. The lesson plan should be designed for a 60-minute class session and should cater to a specific grade level or age group. Begin by stating the lesson objectives, which should be clear, measurable, and aligned with relevant educational standards. Next, provide a detailed outline of the lesson, breaking it down into an introduction, main activities, and a conclusion. For each section, describe the teaching methods, learning activities, and resources you will use to effectively convey the content and engage the students. Finally, describe the assessment methods you will employ to evaluate students' understanding and mastery of the lesson objectives. The lesson plan should be well-organized, easy to follow, and promote active learning and critical thinking. |
| User   | Subject: Introduction to Photosynthesis Grade Level: 7th Grade (Ages 12-13)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

## Example output

> Lesson Plan: Introduction to Photosynthesis
> Grade Level: 7th Grade (Ages 12-13)
> Duration: 60 minutes
>
> Lesson Objectives:
> By the end of the lesson, students will be able to:
>
> 1. Define photosynthesis and explain its importance in the ecosystem.
> 2. Identify the key components necessary for photosynthesis to occur.
> 3. Describe the process of photosynthesis, including the roles of light energy, carbon dioxide, and water.
> 4. Recognize the products of photosynthesis and their significance for living organisms.
>    Lesson Outline:
>
> 5. Introduction (10 minutes)
>    i. Engage students by showing a short video clip or images of plants and discussing their role in the environment.
>    ii. Introduce the concept of photosynthesis and its importance in sustaining life on Earth.
>    iii. State the lesson objectives and provide an overview of the lesson structure.
> 6. Main Activities (40 minutes)
>    i. Guided Instruction (15 minutes)
>    a. Explain the key components necessary for photosynthesis: sunlight, carbon dioxide, water, and chlorophyll.
>    b. Describe the process of photosynthesis, emphasizing the roles of light energy, carbon dioxide, and water.
>    c. Discuss the products of photosynthesis (glucose and oxygen) and their significance for living organisms.
>    ii. Small Group Activity (15 minutes)
>    a. Divide the class into small groups and provide each group with a worksheet or graphic organizer.
>    b. Ask students to work together to create a visual representation of the photosynthesis process, labeling the key components and products.
>    c. Encourage students to discuss and explain their understanding of photosynthesis within their groups.
>    iii. Class Discussion (10 minutes)
>    a. Invite each group to share their visual representation with the class.
>    b. Facilitate a class discussion, encouraging students to ask questions, provide feedback, and clarify any misconceptions.
> 7. Conclusion (10 minutes)
>    i. Summarize the key points of the lesson, reinforcing the definition, components, process, and products of photosynthesis.
>    ii. Administer a short quiz or exit ticket to assess students' understanding of the lesson objectives.
>    iii. Provide students with a homework assignment to further explore the importance of photosynthesis in different ecosystems.
>    Assessment Methods:
>
> 8. Formative assessment: Observe student participation and understanding during the guided instruction and small group activity.
> 9. Summative assessment: Evaluate students' visual representations and their performance on the short quiz or exit ticket.
> 10. Homework assignment: Review students' homework submissions to gauge their ability to apply the concepts learned in the lesson.
>     Resources:
>
> 11. Video clip or images of plants and their role in the environment
> 12. Worksheets or graphic organizers for the small group activity
> 13. Short quiz or exit ticket for assessment
> 14. Homework assignment instructions

### API request

<CodeGroup>
    ```python Python
    import anthropic
    
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="my_api_key",
    )
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4000,
        temperature=0.5,
        system="Your task is to create a comprehensive, engaging, and well-structured lesson plan on the given subject. The lesson plan should be designed for a 60-minute class session and should cater to a specific grade level or age group. Begin by stating the lesson objectives, which should be clear, measurable, and aligned with relevant educational standards. Next, provide a detailed outline of the lesson, breaking it down into an introduction, main activities, and a conclusion. For each section, describe the teaching methods, learning activities, and resources you will use to effectively convey the content and engage the students. Finally, describe the assessment methods you will employ to evaluate students' understanding and mastery of the lesson objectives. The lesson plan should be well-organized, easy to follow, and promote active learning and critical thinking.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Subject: Introduction to Photosynthesis  \nGrade Level: 7th Grade (Ages 12-13)"
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript TypeScript
    import Anthropic from "@anthropic-ai/sdk";
    
    const anthropic = new Anthropic({
      apiKey: "my_api_key", // defaults to process.env["ANTHROPIC_API_KEY"]
    });
    
    const msg = await anthropic.messages.create({
      model: "claude-sonnet-4-5",
      max_tokens: 4000,
      temperature: 0.5,
      system: "Your task is to create a comprehensive, engaging, and well-structured lesson plan on the given subject. The lesson plan should be designed for a 60-minute class session and should cater to a specific grade level or age group. Begin by stating the lesson objectives, which should be clear, measurable, and aligned with relevant educational standards. Next, provide a detailed outline of the lesson, breaking it down into an introduction, main activities, and a conclusion. For each section, describe the teaching methods, learning activities, and resources you will use to effectively convey the content and engage the students. Finally, describe the assessment methods you will employ to evaluate students' understanding and mastery of the lesson objectives. The lesson plan should be well-organized, easy to follow, and promote active learning and critical thinking.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Subject: Introduction to Photosynthesis  \nGrade Level: 7th Grade (Ages 12-13)"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
    
    
    ```python AWS Bedrock Python
    from anthropic import AnthropicBedrock
    
    # See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
    # for authentication options
    client = AnthropicBedrock()
    
    message = client.messages.create(
        model="anthropic.claude-sonnet-4-5-20250929-v1:0",
        max_tokens=4000,
        temperature=0.5,
        system="Your task is to create a comprehensive, engaging, and well-structured lesson plan on the given subject. The lesson plan should be designed for a 60-minute class session and should cater to a specific grade level or age group. Begin by stating the lesson objectives, which should be clear, measurable, and aligned with relevant educational standards. Next, provide a detailed outline of the lesson, breaking it down into an introduction, main activities, and a conclusion. For each section, describe the teaching methods, learning activities, and resources you will use to effectively convey the content and engage the students. Finally, describe the assessment methods you will employ to evaluate students' understanding and mastery of the lesson objectives. The lesson plan should be well-organized, easy to follow, and promote active learning and critical thinking.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Subject: Introduction to Photosynthesis  \nGrade Level: 7th Grade (Ages 12-13)"
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript AWS Bedrock TypeScript
    import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";
    
    // See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
    // for authentication options
    const client = new AnthropicBedrock();
    
    const msg = await client.messages.create({
      model: "anthropic.claude-sonnet-4-5-20250929-v1:0",
      max_tokens: 4000,
      temperature: 0.5,
      system: "Your task is to create a comprehensive, engaging, and well-structured lesson plan on the given subject. The lesson plan should be designed for a 60-minute class session and should cater to a specific grade level or age group. Begin by stating the lesson objectives, which should be clear, measurable, and aligned with relevant educational standards. Next, provide a detailed outline of the lesson, breaking it down into an introduction, main activities, and a conclusion. For each section, describe the teaching methods, learning activities, and resources you will use to effectively convey the content and engage the students. Finally, describe the assessment methods you will employ to evaluate students' understanding and mastery of the lesson objectives. The lesson plan should be well-organized, easy to follow, and promote active learning and critical thinking.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Subject: Introduction to Photosynthesis  \nGrade Level: 7th Grade (Ages 12-13)"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
    
    
    ```python Vertex AI Python
    from anthropic import AnthropicVertex
    
    client = AnthropicVertex()
    
    message = client.messages.create(
        model="claude-sonnet-4@20250514",
        max_tokens=4000,
        temperature=0.5,
        system="Your task is to create a comprehensive, engaging, and well-structured lesson plan on the given subject. The lesson plan should be designed for a 60-minute class session and should cater to a specific grade level or age group. Begin by stating the lesson objectives, which should be clear, measurable, and aligned with relevant educational standards. Next, provide a detailed outline of the lesson, breaking it down into an introduction, main activities, and a conclusion. For each section, describe the teaching methods, learning activities, and resources you will use to effectively convey the content and engage the students. Finally, describe the assessment methods you will employ to evaluate students' understanding and mastery of the lesson objectives. The lesson plan should be well-organized, easy to follow, and promote active learning and critical thinking.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Subject: Introduction to Photosynthesis  \nGrade Level: 7th Grade (Ages 12-13)"
                    }
                ]
            }
        ]
    )
    print(message.content)
    
    ```
    
    
    ```typescript Vertex AI TypeScript
    import { AnthropicVertex } from '@anthropic-ai/vertex-sdk';
    
    // Reads from the `CLOUD_ML_REGION` & `ANTHROPIC_VERTEX_PROJECT_ID` environment variables.
    // Additionally goes through the standard `google-auth-library` flow.
    const client = new AnthropicVertex();
    
    const msg = await client.messages.create({
      model: "claude-sonnet-4@20250514",
      max_tokens: 4000,
      temperature: 0.5,
      system: "Your task is to create a comprehensive, engaging, and well-structured lesson plan on the given subject. The lesson plan should be designed for a 60-minute class session and should cater to a specific grade level or age group. Begin by stating the lesson objectives, which should be clear, measurable, and aligned with relevant educational standards. Next, provide a detailed outline of the lesson, breaking it down into an introduction, main activities, and a conclusion. For each section, describe the teaching methods, learning activities, and resources you will use to effectively convey the content and engage the students. Finally, describe the assessment methods you will employ to evaluate students' understanding and mastery of the lesson objectives. The lesson plan should be well-organized, easy to follow, and promote active learning and critical thinking.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Subject: Introduction to Photosynthesis  \nGrade Level: 7th Grade (Ages 12-13)"
            }
          ]
        }
      ]
    });
    console.log(msg);
    
    ```
</CodeGroup>