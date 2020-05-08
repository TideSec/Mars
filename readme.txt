1、在Mac上创建任务线程出错
 错误提示：OSX crash complaining of operation `in progress in another thread when fork() was called
 解决办法：export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES