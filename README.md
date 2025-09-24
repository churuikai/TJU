# 免责声明
Tianjin University Course Selection System External Interface (For personal study use only, please do not use for automated course selection, etc.)

## 环境准备
1. 安装 [Python 3.7+](https://www.python.org/downloads/)。
2. 安装依赖库：
   ```powershell
   pip install requests pyyaml


## 使用说明

1. 点击右上角 `star` `ヾ(*>∀＜*)(ﾉ∀｀●)⊃`
<img width="48" height="48" alt="0792EE16" src="https://github.com/user-attachments/assets/0fdb1562-00c1-4281-9ebf-faa008091876" />

2. **编辑 `config.yaml`**  
   
   - 在 `schedule` 下配置预计开始运行的时间（hour、minute）。  
   - 在 `request` 下填写接口和鉴权信息（例如 `url`、`cookie`）。 
   - 在 `courses` 下列出需要选的课程编码（课程编码⚠️非课程代码非课程序号）。
   
   > `url`、`cookie`、`课程代码` 获取方法：
   >
   > 在选课系统半开放时（预选课阶段），登录选课系统。然后打开F12调试模式，点击`网络(network)` 捕获请求。
   >
   > 搜索需要选择的课程，点击选课、提交。此时系统提示未到选课时间，系统未开放，但已经捕获到选课请求（一般是最新、最后一条记录，开头为stdElectCourse.....）。
   >
   > 点击该请求，在标头（header）查看 `url`、 `cookie` 、在负载（payload）中可以查看该课程编号。
   >
   > 注：url和cookie是一样的，课程的编号则需要单独捕获。
   


3. **运行脚本**  
   
   - 运行 `main.py` 或终端执行：
     ```powershell
     python main.py
     ```
   - 代码将在指定时间自动发送选课请求，并按顺序尝试选课。
   
4. **运行机制**    
   - 使用配置的请求头和课程编号依次尝试选课，如果选课成功则移除对应课程；若失败会轮询重试。  
   - 会导出日志信息。
