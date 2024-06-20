//alert("登录成功加载")

// 验证码获取点击事件绑定
function bindEmailCaptchaClick(){
    $("#captcha-btn").click(function (event) {
       //&this: 代表的是当前按钮的 jquery 对象
        var $this = $(this);

        //阻止默认事件
        event.preventDefault();
        var email = $("input[name='email']").val();

        if(!email){  // 未输入邮箱
            alert("请先输入注册邮箱！")
        }
        else{
             $.ajax({
            url: "/captcha/email?email=" + email,
            //method: "GET",
            type: "GET",
            success: function (result) {
                var code = result['code'];
                if (code == 200){
                   var countdown = 60;
                   //开始倒计时之前，取消按钮的点击事件
                    $this.off("click");
                    var timer = setInterval(function (){
                       $this.text(countdown);  //修改倒计时
                       countdown -= 1;
                       // 倒计时结束的时候执行
                        if(countdown <= 0){
                            //清除定时器
                            clearInterval(timer);
                            //将按钮的文字重新修改回来
                            $this.text("获取验证码");
                            //重新绑定点击事件
                            bindEmailCaptchaClick();
                        }
                   }, 1000);  //每间隔 1 秒执行函数
                    alert("邮箱验证码已发送，请注意查收")
                }else {
                    alert(result['message']);
                }
                console.log(result)
            },
            fail: function (error) {
                console.log(error);
            }
        })
        }
    });
}


// 等整个网页加载完成后再执行
$(function () {
    bindEmailCaptchaClick();
});