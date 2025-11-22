# Meeting scribe

Distill meetings into concise summaries including discussion topics, key takeaways, and action items.

---

> Copy this prompt into our developer [Console](/dashboard) to try it for yourself!

|        | Content                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System | Your task is to review the provided meeting notes and create a concise summary that captures the essential information, focusing on key takeaways and action items assigned to specific individuals or departments during the meeting. Use clear and professional language, and organize the summary in a logical manner using appropriate formatting such as headings, subheadings, and bullet points. Ensure that the summary is easy to understand and provides a comprehensive but succinct overview of the meeting's content, with a particular focus on clearly indicating who is responsible for each action item.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| User   | Meeting notes: <br/> <br/> Date: Verona, Italy - Late 16th century <br/><br/> Attendees: <br/> - Lord Capulet (Head of the Capulet family) <br/> - Lord Montague (Head of the Montague family) <br/> - Prince Escalus (Ruler of Verona) <br/> - Friar Laurence (Religious advisor) <br/><br/> Agenda: <br/> 1. Address the ongoing feud between the Capulet and Montague families <br/> 2. Discuss the secret marriage of Romeo Montague and Juliet Capulet <br/> 3. Develop a plan to bring peace to Verona <br/> 4. Address the tragic deaths of Romeo and Juliet <br/><br/> Discussion: <br/> - Prince Escalus opened the meeting by expressing his grave concern over the long-standing feud between the Capulet and Montague families. He admonished both Lord Capulet and Lord Montague for the recent violent clashes that have disturbed the peace in Verona's streets. The Prince warned that further violence would result in severe consequences, including heavy fines and potential exile for the perpetrators. <br/> - Friar Laurence then broached the topic of the between Romeo Montague and Juliet Capulet, which had taken place under his guidance. Lord Capulet and Lord Montague evidently had not known about it, and reacted with anger and disbelief. However, Friar Laurence urged them to consider the profound and tragic love shared by their children and the potential for this love to heal the rift between the families going forward. <br/> - Prince Escalus proposed a formal truce between the Capulet and Montague families. He demanded that both sides lay down their arms and cease all hostile actions against one another. The Prince declared that any violation of the truce would result in severe punishments, including the possibility of exile or even execution. Lord Capulet and Lord Montague, recognizing the wisdom in the Prince's words and the necessity of peace for the well-being of their families and the city, grudgingly agreed to the terms of the truce. <br/> - The meeting took a somber turn as the tragic deaths of Romeo and Juliet were addressed. Friar Laurence recounted the unfortunate series of events that led to the young lovers taking their own lives, emphasizing the devastating impact of the families' hatred on their innocent children. Lord Capulet and Lord Montague, overcome with grief and remorse, acknowledged that their blind hatred had ultimately caused the loss of their beloved children. <br/>- Prince Escalus called upon the families to learn from this heartbreaking tragedy and to embrace forgiveness and unity in honor of Romeo and Juliet's memory. He urged them to work together to create a lasting peace in Verona, setting aside their long-standing animosity. Friar Laurence offered his support in mediating any future disputes and providing spiritual guidance to help the families heal and move forward. <br/>- As the meeting drew to a close, Lord Capulet and Lord Montague pledged to put an end to their feud and work towards reconciliation. Prince Escalus reaffirmed his commitment to ensuring that the truce would be upheld, promising swift justice for any who dared to break it. <br/>- The attendees agreed to meet regularly to discuss the progress of their reconciliation efforts and to address any challenges that may arise. |

## Example Output

Meeting Summary: Reconciliation and Peace in Verona
Date: Late 16th century, Verona, Italy

Attendees:

    - Lord Capulet (Head of the Capulet family)
    - Lord Montague (Head of the Montague family)
    - Prince Escalus (Ruler of Verona)
    - Friar Laurence (Religious advisor)

Key Takeaways:

    - Prince Escalus addressed the ongoing feud between the Capulet and Montague families, warning of severe consequences for further violence.
    - Friar Laurence revealed the secret marriage between Romeo Montague and Juliet Capulet, urging the families to consider the potential for their love to heal the rift.
    - Prince Escalus proposed a formal truce between the families, threatening severe punishments for any violations.
    - The tragic deaths of Romeo and Juliet were discussed, with Lord Capulet and Lord Montague acknowledging their role in the heartbreaking outcome.
    - Prince Escalus called for forgiveness and unity in honor of Romeo and Juliet's memory, urging the families to work together for lasting peace in Verona.

Action Items:

- Lord Capulet and Lord Montague:
  - Lay down arms and cease all hostile actions against one another.
  - Work towards reconciliation and embrace forgiveness.
  - Attend regular meetings to discuss progress and address challenges.
- Prince Escalus:
  - Enforce the truce and ensure its adherence.
  - Administer swift justice for any violations of the truce.
- Friar Laurence:
  - Provide mediation and spiritual guidance to support the families in their healing and reconciliation process.

Next Steps:

- The attendees will meet regularly to monitor the progress of reconciliation efforts and address any arising challenges.

## API request

<Tabs>
<Tab title="Python">

```python
import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my_api_key",
)
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4000,
    temperature=0.5,
    system="Your task is to review the provided meeting notes and create a concise summary that captures the essential information, focusing on key takeaways and action items assigned to specific individuals or departments during the meeting. Use clear and professional language, and organize the summary in a logical manner using appropriate formatting such as headings, subheadings, and bullet points. Ensure that the summary is easy to understand and provides a comprehensive but succinct overview of the meeting's content, with a particular focus on clearly indicating who is responsible for each action item.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Meeting notes:  \n  \nDate: Verona, Italy - Late 16th century  \n  \nAttendees:  \n- Lord Capulet (Head of the Capulet family)  \n- Lord Montague (Head of the Montague family)  \n- Prince Escalus (Ruler of Verona)  \n- Friar Laurence (Religious advisor)  \n  \nAgenda:  \n1. Address the ongoing feud between the Capulet and Montague families  \n2. Discuss the secret marriage of Romeo Montague and Juliet Capulet  \n3. Develop a plan to bring peace to Verona  \n4. Address the tragic deaths of Romeo and Juliet  \n  \nDiscussion:  \n- Prince Escalus opened the meeting by expressing his grave concern over the long-standing feud between the Capulet and Montague families. He admonished both Lord Capulet and Lord Montague for the recent violent clashes that have disturbed the peace in Verona's streets. The Prince warned that further violence would result in severe consequences, including heavy fines and potential exile for the perpetrators.  \n- Friar Laurence then broached the topic of the between Romeo Montague and Juliet Capulet, which had taken place under his guidance. Lord Capulet and Lord Montague evidently had not known about it, and reacted with anger and disbelief. However, Friar Laurence urged them to consider the profound and tragic love shared by their children and the potential for this love to heal the rift between the families going forward.  \n- Prince Escalus proposed a formal truce between the Capulet and Montague families. He demanded that both sides lay down their arms and cease all hostile actions against one another. The Prince declared that any violation of the truce would result in severe punishments, including the possibility of exile or even execution. Lord Capulet and Lord Montague, recognizing the wisdom in the Prince's words and the necessity of peace for the well-being of their families and the city, grudgingly agreed to the terms of the truce.  \n- The meeting took a somber turn as the tragic deaths of Romeo and Juliet were addressed. Friar Laurence recounted the unfortunate series of events that led to the young lovers taking their own lives, emphasizing the devastating impact of the families' hatred on their innocent children. Lord Capulet and Lord Montague, overcome with grief and remorse, acknowledged that their blind hatred had ultimately caused the loss of their beloved children.  \n- Prince Escalus called upon the families to learn from this heartbreaking tragedy and to embrace forgiveness and unity in honor of Romeo and Juliet's memory. He urged them to work together to create a lasting peace in Verona, setting aside their long-standing animosity. Friar Laurence offered his support in mediating any future disputes and providing spiritual guidance to help the families heal and move forward.  \n- As the meeting drew to a close, Lord Capulet and Lord Montague pledged to put an end to their feud and work towards reconciliation. Prince Escalus reaffirmed his commitment to ensuring that the truce would be upheld, promising swift justice for any who dared to break it.  \n- The attendees agreed to meet regularly to discuss the progress of their reconciliation efforts and to address any challenges that may arise."
                }
            ]
        }
    ]
)
print(message.content)

```

</Tab>
<Tab title="TypeScript">

```typescript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: "my_api_key", // defaults to process.env["ANTHROPIC_API_KEY"]
});

const msg = await anthropic.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 4000,
  temperature: 0.5,
  system: "Your task is to review the provided meeting notes and create a concise summary that captures the essential information, focusing on key takeaways and action items assigned to specific individuals or departments during the meeting. Use clear and professional language, and organize the summary in a logical manner using appropriate formatting such as headings, subheadings, and bullet points. Ensure that the summary is easy to understand and provides a comprehensive but succinct overview of the meeting's content, with a particular focus on clearly indicating who is responsible for each action item.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Meeting notes:  \n  \nDate: Verona, Italy - Late 16th century  \n  \nAttendees:  \n- Lord Capulet (Head of the Capulet family)  \n- Lord Montague (Head of the Montague family)  \n- Prince Escalus (Ruler of Verona)  \n- Friar Laurence (Religious advisor)  \n  \nAgenda:  \n1. Address the ongoing feud between the Capulet and Montague families  \n2. Discuss the secret marriage of Romeo Montague and Juliet Capulet  \n3. Develop a plan to bring peace to Verona  \n4. Address the tragic deaths of Romeo and Juliet  \n  \nDiscussion:  \n- Prince Escalus opened the meeting by expressing his grave concern over the long-standing feud between the Capulet and Montague families. He admonished both Lord Capulet and Lord Montague for the recent violent clashes that have disturbed the peace in Verona's streets. The Prince warned that further violence would result in severe consequences, including heavy fines and potential exile for the perpetrators.  \n- Friar Laurence then broached the topic of the between Romeo Montague and Juliet Capulet, which had taken place under his guidance. Lord Capulet and Lord Montague evidently had not known about it, and reacted with anger and disbelief. However, Friar Laurence urged them to consider the profound and tragic love shared by their children and the potential for this love to heal the rift between the families going forward.  \n- Prince Escalus proposed a formal truce between the Capulet and Montague families. He demanded that both sides lay down their arms and cease all hostile actions against one another. The Prince declared that any violation of the truce would result in severe punishments, including the possibility of exile or even execution. Lord Capulet and Lord Montague, recognizing the wisdom in the Prince's words and the necessity of peace for the well-being of their families and the city, grudgingly agreed to the terms of the truce.  \n- The meeting took a somber turn as the tragic deaths of Romeo and Juliet were addressed. Friar Laurence recounted the unfortunate series of events that led to the young lovers taking their own lives, emphasizing the devastating impact of the families' hatred on their innocent children. Lord Capulet and Lord Montague, overcome with grief and remorse, acknowledged that their blind hatred had ultimately caused the loss of their beloved children.  \n- Prince Escalus called upon the families to learn from this heartbreaking tragedy and to embrace forgiveness and unity in honor of Romeo and Juliet's memory. He urged them to work together to create a lasting peace in Verona, setting aside their long-standing animosity. Friar Laurence offered his support in mediating any future disputes and providing spiritual guidance to help the families heal and move forward.  \n- As the meeting drew to a close, Lord Capulet and Lord Montague pledged to put an end to their feud and work towards reconciliation. Prince Escalus reaffirmed his commitment to ensuring that the truce would be upheld, promising swift justice for any who dared to break it.  \n- The attendees agreed to meet regularly to discuss the progress of their reconciliation efforts and to address any challenges that may arise."
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
<Tab title="AWS Bedrock Python">

```python
from anthropic import AnthropicBedrock

# See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
# for authentication options
client = AnthropicBedrock()

message = client.messages.create(
    model="anthropic.claude-sonnet-4-5-20250929-v1:0",
    max_tokens=4000,
    temperature=0.5,
    system="Your task is to review the provided meeting notes and create a concise summary that captures the essential information, focusing on key takeaways and action items assigned to specific individuals or departments during the meeting. Use clear and professional language, and organize the summary in a logical manner using appropriate formatting such as headings, subheadings, and bullet points. Ensure that the summary is easy to understand and provides a comprehensive but succinct overview of the meeting's content, with a particular focus on clearly indicating who is responsible for each action item.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Meeting notes:  \n  \nDate: Verona, Italy - Late 16th century  \n  \nAttendees:  \n- Lord Capulet (Head of the Capulet family)  \n- Lord Montague (Head of the Montague family)  \n- Prince Escalus (Ruler of Verona)  \n- Friar Laurence (Religious advisor)  \n  \nAgenda:  \n1. Address the ongoing feud between the Capulet and Montague families  \n2. Discuss the secret marriage of Romeo Montague and Juliet Capulet  \n3. Develop a plan to bring peace to Verona  \n4. Address the tragic deaths of Romeo and Juliet  \n  \nDiscussion:  \n- Prince Escalus opened the meeting by expressing his grave concern over the long-standing feud between the Capulet and Montague families. He admonished both Lord Capulet and Lord Montague for the recent violent clashes that have disturbed the peace in Verona's streets. The Prince warned that further violence would result in severe consequences, including heavy fines and potential exile for the perpetrators.  \n- Friar Laurence then broached the topic of the between Romeo Montague and Juliet Capulet, which had taken place under his guidance. Lord Capulet and Lord Montague evidently had not known about it, and reacted with anger and disbelief. However, Friar Laurence urged them to consider the profound and tragic love shared by their children and the potential for this love to heal the rift between the families going forward.  \n- Prince Escalus proposed a formal truce between the Capulet and Montague families. He demanded that both sides lay down their arms and cease all hostile actions against one another. The Prince declared that any violation of the truce would result in severe punishments, including the possibility of exile or even execution. Lord Capulet and Lord Montague, recognizing the wisdom in the Prince's words and the necessity of peace for the well-being of their families and the city, grudgingly agreed to the terms of the truce.  \n- The meeting took a somber turn as the tragic deaths of Romeo and Juliet were addressed. Friar Laurence recounted the unfortunate series of events that led to the young lovers taking their own lives, emphasizing the devastating impact of the families' hatred on their innocent children. Lord Capulet and Lord Montague, overcome with grief and remorse, acknowledged that their blind hatred had ultimately caused the loss of their beloved children.  \n- Prince Escalus called upon the families to learn from this heartbreaking tragedy and to embrace forgiveness and unity in honor of Romeo and Juliet's memory. He urged them to work together to create a lasting peace in Verona, setting aside their long-standing animosity. Friar Laurence offered his support in mediating any future disputes and providing spiritual guidance to help the families heal and move forward.  \n- As the meeting drew to a close, Lord Capulet and Lord Montague pledged to put an end to their feud and work towards reconciliation. Prince Escalus reaffirmed his commitment to ensuring that the truce would be upheld, promising swift justice for any who dared to break it.  \n- The attendees agreed to meet regularly to discuss the progress of their reconciliation efforts and to address any challenges that may arise."
                }
            ]
        }
    ]
)
print(message.content)

```

</Tab>
<Tab title="AWS Bedrock TypeScript">

```typescript
import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

// See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
// for authentication options
const client = new AnthropicBedrock();

const msg = await client.messages.create({
  model: "anthropic.claude-sonnet-4-5-20250929-v1:0",
  max_tokens: 4000,
  temperature: 0.5,
  system: "Your task is to review the provided meeting notes and create a concise summary that captures the essential information, focusing on key takeaways and action items assigned to specific individuals or departments during the meeting. Use clear and professional language, and organize the summary in a logical manner using appropriate formatting such as headings, subheadings, and bullet points. Ensure that the summary is easy to understand and provides a comprehensive but succinct overview of the meeting's content, with a particular focus on clearly indicating who is responsible for each action item.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Meeting notes:  \n  \nDate: Verona, Italy - Late 16th century  \n  \nAttendees:  \n- Lord Capulet (Head of the Capulet family)  \n- Lord Montague (Head of the Montague family)  \n- Prince Escalus (Ruler of Verona)  \n- Friar Laurence (Religious advisor)  \n  \nAgenda:  \n1. Address the ongoing feud between the Capulet and Montague families  \n2. Discuss the secret marriage of Romeo Montague and Juliet Capulet  \n3. Develop a plan to bring peace to Verona  \n4. Address the tragic deaths of Romeo and Juliet  \n  \nDiscussion:  \n- Prince Escalus opened the meeting by expressing his grave concern over the long-standing feud between the Capulet and Montague families. He admonished both Lord Capulet and Lord Montague for the recent violent clashes that have disturbed the peace in Verona's streets. The Prince warned that further violence would result in severe consequences, including heavy fines and potential exile for the perpetrators.  \n- Friar Laurence then broached the topic of the between Romeo Montague and Juliet Capulet, which had taken place under his guidance. Lord Capulet and Lord Montague evidently had not known about it, and reacted with anger and disbelief. However, Friar Laurence urged them to consider the profound and tragic love shared by their children and the potential for this love to heal the rift between the families going forward.  \n- Prince Escalus proposed a formal truce between the Capulet and Montague families. He demanded that both sides lay down their arms and cease all hostile actions against one another. The Prince declared that any violation of the truce would result in severe punishments, including the possibility of exile or even execution. Lord Capulet and Lord Montague, recognizing the wisdom in the Prince's words and the necessity of peace for the well-being of their families and the city, grudgingly agreed to the terms of the truce.  \n- The meeting took a somber turn as the tragic deaths of Romeo and Juliet were addressed. Friar Laurence recounted the unfortunate series of events that led to the young lovers taking their own lives, emphasizing the devastating impact of the families' hatred on their innocent children. Lord Capulet and Lord Montague, overcome with grief and remorse, acknowledged that their blind hatred had ultimately caused the loss of their beloved children.  \n- Prince Escalus called upon the families to learn from this heartbreaking tragedy and to embrace forgiveness and unity in honor of Romeo and Juliet's memory. He urged them to work together to create a lasting peace in Verona, setting aside their long-standing animosity. Friar Laurence offered his support in mediating any future disputes and providing spiritual guidance to help the families heal and move forward.  \n- As the meeting drew to a close, Lord Capulet and Lord Montague pledged to put an end to their feud and work towards reconciliation. Prince Escalus reaffirmed his commitment to ensuring that the truce would be upheld, promising swift justice for any who dared to break it.  \n- The attendees agreed to meet regularly to discuss the progress of their reconciliation efforts and to address any challenges that may arise."
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
<Tab title="Vertex AI Python">

```python
from anthropic import AnthropicVertex

client = AnthropicVertex()

message = client.messages.create(
    model="claude-sonnet-4@20250514",
    max_tokens=4000,
    temperature=0.5,
    system="Your task is to review the provided meeting notes and create a concise summary that captures the essential information, focusing on key takeaways and action items assigned to specific individuals or departments during the meeting. Use clear and professional language, and organize the summary in a logical manner using appropriate formatting such as headings, subheadings, and bullet points. Ensure that the summary is easy to understand and provides a comprehensive but succinct overview of the meeting's content, with a particular focus on clearly indicating who is responsible for each action item.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Meeting notes:  \n  \nDate: Verona, Italy - Late 16th century  \n  \nAttendees:  \n- Lord Capulet (Head of the Capulet family)  \n- Lord Montague (Head of the Montague family)  \n- Prince Escalus (Ruler of Verona)  \n- Friar Laurence (Religious advisor)  \n  \nAgenda:  \n1. Address the ongoing feud between the Capulet and Montague families  \n2. Discuss the secret marriage of Romeo Montague and Juliet Capulet  \n3. Develop a plan to bring peace to Verona  \n4. Address the tragic deaths of Romeo and Juliet  \n  \nDiscussion:  \n- Prince Escalus opened the meeting by expressing his grave concern over the long-standing feud between the Capulet and Montague families. He admonished both Lord Capulet and Lord Montague for the recent violent clashes that have disturbed the peace in Verona's streets. The Prince warned that further violence would result in severe consequences, including heavy fines and potential exile for the perpetrators.  \n- Friar Laurence then broached the topic of the between Romeo Montague and Juliet Capulet, which had taken place under his guidance. Lord Capulet and Lord Montague evidently had not known about it, and reacted with anger and disbelief. However, Friar Laurence urged them to consider the profound and tragic love shared by their children and the potential for this love to heal the rift between the families going forward.  \n- Prince Escalus proposed a formal truce between the Capulet and Montague families. He demanded that both sides lay down their arms and cease all hostile actions against one another. The Prince declared that any violation of the truce would result in severe punishments, including the possibility of exile or even execution. Lord Capulet and Lord Montague, recognizing the wisdom in the Prince's words and the necessity of peace for the well-being of their families and the city, grudgingly agreed to the terms of the truce.  \n- The meeting took a somber turn as the tragic deaths of Romeo and Juliet were addressed. Friar Laurence recounted the unfortunate series of events that led to the young lovers taking their own lives, emphasizing the devastating impact of the families' hatred on their innocent children. Lord Capulet and Lord Montague, overcome with grief and remorse, acknowledged that their blind hatred had ultimately caused the loss of their beloved children.  \n- Prince Escalus called upon the families to learn from this heartbreaking tragedy and to embrace forgiveness and unity in honor of Romeo and Juliet's memory. He urged them to work together to create a lasting peace in Verona, setting aside their long-standing animosity. Friar Laurence offered his support in mediating any future disputes and providing spiritual guidance to help the families heal and move forward.  \n- As the meeting drew to a close, Lord Capulet and Lord Montague pledged to put an end to their feud and work towards reconciliation. Prince Escalus reaffirmed his commitment to ensuring that the truce would be upheld, promising swift justice for any who dared to break it.  \n- The attendees agreed to meet regularly to discuss the progress of their reconciliation efforts and to address any challenges that may arise."
                }
            ]
        }
    ]
)
print(message.content)

```

</Tab>
<Tab title="Vertex AI TypeScript">

```typescript
import { AnthropicVertex } from '@anthropic-ai/vertex-sdk';

// Reads from the `CLOUD_ML_REGION` & `ANTHROPIC_VERTEX_PROJECT_ID` environment variables.
// Additionally goes through the standard `google-auth-library` flow.
const client = new AnthropicVertex();

const msg = await client.messages.create({
  model: "claude-sonnet-4@20250514",
  max_tokens: 4000,
  temperature: 0.5,
  system: "Your task is to review the provided meeting notes and create a concise summary that captures the essential information, focusing on key takeaways and action items assigned to specific individuals or departments during the meeting. Use clear and professional language, and organize the summary in a logical manner using appropriate formatting such as headings, subheadings, and bullet points. Ensure that the summary is easy to understand and provides a comprehensive but succinct overview of the meeting's content, with a particular focus on clearly indicating who is responsible for each action item.",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Meeting notes:  \n  \nDate: Verona, Italy - Late 16th century  \n  \nAttendees:  \n- Lord Capulet (Head of the Capulet family)  \n- Lord Montague (Head of the Montague family)  \n- Prince Escalus (Ruler of Verona)  \n- Friar Laurence (Religious advisor)  \n  \nAgenda:  \n1. Address the ongoing feud between the Capulet and Montague families  \n2. Discuss the secret marriage of Romeo Montague and Juliet Capulet  \n3. Develop a plan to bring peace to Verona  \n4. Address the tragic deaths of Romeo and Juliet  \n  \nDiscussion:  \n- Prince Escalus opened the meeting by expressing his grave concern over the long-standing feud between the Capulet and Montague families. He admonished both Lord Capulet and Lord Montague for the recent violent clashes that have disturbed the peace in Verona's streets. The Prince warned that further violence would result in severe consequences, including heavy fines and potential exile for the perpetrators.  \n- Friar Laurence then broached the topic of the between Romeo Montague and Juliet Capulet, which had taken place under his guidance. Lord Capulet and Lord Montague evidently had not known about it, and reacted with anger and disbelief. However, Friar Laurence urged them to consider the profound and tragic love shared by their children and the potential for this love to heal the rift between the families going forward.  \n- Prince Escalus proposed a formal truce between the Capulet and Montague families. He demanded that both sides lay down their arms and cease all hostile actions against one another. The Prince declared that any violation of the truce would result in severe punishments, including the possibility of exile or even execution. Lord Capulet and Lord Montague, recognizing the wisdom in the Prince's words and the necessity of peace for the well-being of their families and the city, grudgingly agreed to the terms of the truce.  \n- The meeting took a somber turn as the tragic deaths of Romeo and Juliet were addressed. Friar Laurence recounted the unfortunate series of events that led to the young lovers taking their own lives, emphasizing the devastating impact of the families' hatred on their innocent children. Lord Capulet and Lord Montague, overcome with grief and remorse, acknowledged that their blind hatred had ultimately caused the loss of their beloved children.  \n- Prince Escalus called upon the families to learn from this heartbreaking tragedy and to embrace forgiveness and unity in honor of Romeo and Juliet's memory. He urged them to work together to create a lasting peace in Verona, setting aside their long-standing animosity. Friar Laurence offered his support in mediating any future disputes and providing spiritual guidance to help the families heal and move forward.  \n- As the meeting drew to a close, Lord Capulet and Lord Montague pledged to put an end to their feud and work towards reconciliation. Prince Escalus reaffirmed his commitment to ensuring that the truce would be upheld, promising swift justice for any who dared to break it.  \n- The attendees agreed to meet regularly to discuss the progress of their reconciliation efforts and to address any challenges that may arise."
        }
      ]
    }
  ]
});
console.log(msg);

```

</Tab>
</Tabs>