# GPT_SoVits-ECNU-llm
采用ECNU大模型（采用其他openai api接口同样可以使用）做的一个pyhton对话智能体，Prompt可以修改

# 使用说明
1.如若需要采用GPT—Sovits的模型，需要在后台打开GPT—Sovits的API接口，我采用的是在GPT—Sovits根目录下添加了一个api.bat(编辑方式参考go-webui.bat),打开即可使用

2.GPT—Sovits设置了超时关闭（30s内语音未合成自动取消），设置超时限制的时间在tts_client.py中_use_custom_tts函数中

3.可以考虑使用高校发放的大模型api

# 不足之处
1.处女之作，很多地方还是ai完成的，对于api的调用也是一知半解，望谅解

2.GPT—Sovits超时关闭后无法再次合成语音，需要重启

3......

# 联系方式
邮箱：375351298@qq.com



