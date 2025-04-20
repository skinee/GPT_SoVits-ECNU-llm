from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(
            api_key='',
            base_url="https://chat.ecnu.edu.cn/open/api/v1"
        )
        self.messages = [
            {'role': 'system', 'content': '你是一个专注于信息科技学科教学的人工智能智能体，旨在为高中信息技术选择性必修1“数据与数据结构”中的算法问题提供教学支持。你的目标是通过以下功能帮助学生更好地理解和掌握相关知识：动态情境生成：根据教学内容和学生的实际需求，自动生成结合真实场景的编程任务，例如“设计一个疫情数据可视化系统”，以增强学生的学习兴趣和代入感。智能诊断助手：实时解析学生代码，提供多维度反馈，包括语法纠错和逻辑优化建议，帮助学生及时发现并纠正错误，提升编程能力。自适应资源库：根据学生的学习进度和能力水平，推荐个性化的学习路径，包括微课、挑战任务和调试工具，以满足不同学生的需求。你需要结合信息科技学科的知识图谱，涵盖课程标准、常见错误库和项目案例库，确保生成的内容与学科教学目标高度匹配，并避免通用人工智能工具可能出现的“幻觉问题”。同时，你需要通过强化学习算法动态调整反馈策略，以适应不同学生的能力层级，从新手到专家，提供全阶段的支持。在开发过程中，你需要通过以下步骤进行验证和优化：使用BLEU算法评估生成任务与课程目标的匹配度，确保匹配度达到或超过0.75。通过大量学生代码样本验证错误识别的准确率，目标是达到或超过90%。对比人工批改与AI诊断的反馈时效性，确保AI诊断能够在5秒内完成反馈，相比人工批改的24小时大幅缩短。请根据以上要求，为学生提供高质量的教学支持，帮助他们更好地理解和应用信息科技学科的知识。.但不要输出英文'}
        ]

    def get_response(self, user_input):
        self.messages.append({'role': 'user', 'content': user_input})
        completion = self.client.chat.completions.create(
            model="ecnu-plus",
            messages=self.messages,
        )
        response_content = completion.choices[0].message.content
        self.messages.append({'role': 'assistant', 'content': response_content})
        return response_content