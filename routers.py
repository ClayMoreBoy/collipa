# coding: utf-8

from controllers import (site,
                         user,
                         topic,
                         reply,
                         node,
                         image,
                         api,
                         upload,
                         tweet
                        )


routers = [
    (r"/", site.CommunityHandler),
    (r"/timeline", site.TimelineHandler),
    (r"/timeline/public", site.PublicTimelineHandler),
    (r"/account/setting", user.SettingHandler),

    (r"/signup[/]*", user.SignupHandler),
    (r"/signin[/]*", user.SigninHandler),
    (r"/signout[/]*", user.SignoutHandler),

    (r"/notifications[/]*", user.NotificationHandler),
    (r"/messages[/]*", user.MessageHandler),
    (r"/message/create[/]*", user.MessageCreateHandler),

    (r"/users[/]*", user.ShowHandler),

    (r"/topic/(\d+)[/]*", topic.HomeHandler),
    (r"/topic/(\d+)/history[/]*", topic.HistoryHandler),
    (r"/topic/(\d+)/edit[/]*", topic.EditHandler),
    (r"/topic/create[/]*", topic.CreateHandler),

    (r"/node/create[/]*", node.CreateHandler),
    (r"/node/([A-Za-z0-9%_]+)[/]*", node.HomeHandler),
    (r"/node/([A-Za-z0-9%_]+)/edit[/]*", node.EditHandler),
    (r"/node/(\d+)/upload[/]*", node.ImgUploadHandler),
    (r"/node/([A-Za-z0-9%_]+)/(latest|desert|hot|dispute)[/]*", node.HomeHandler),
    (r"/nodes[/]*", node.ShowHandler),

    (r"/reply/create[/]*", reply.CreateHandler),
    (r"/reply/(\d+)[/]*", reply.HomeHandler),
    (r"/reply/(\d+)/edit[/]*", reply.EditHandler),
    (r"/reply/(\d+)/history[/]*", reply.HistoryHandler),

    (r"/tweet/create[/]*", tweet.CreateHandler),
    (r"/tweet/(\d+)[/]*", tweet.HomeHandler),

    (r"/image/(\d+)[/]*", image.HomeHandler),
    (r"/image/upload[/]*", image.UploadHandler),
    (r"/upload/avatar[/]*", user.AvatarUploadHandler),
    (r"/upload/(\w+)[/]*", upload.UploadHandler),
    (r"/account/setting/avatar/crop[/]*", user.AvatarCropHandler),
    (r"/account/upload[/]*", user.ImgUploadHandler),
    (r"/account/password[/]*", user.PasswordHandler),
    (r"/findpassword[/]*", user.FindPasswordHandler),

    (r"/api/getusername[/]*", api.GetUserNameHandler),
    (r"/api/websocket[/]*", api.WebSocketHandler),
    (r"/api/messagewebsocket[/]*", user.MessageCreateHandler),
    (r"/api/mention[/]*", api.MentionHandler),

    (r"/502[/]*", site.PageErrorHandler),
    (r"/302[/]*", site.OtherPageErrorHandler),

    (r"/([A-Za-z0-9%_]+)[/]*", user.HomeHandler),
    (r"/([A-Za-z0-9%_]+)/(topics|replies|followings|followers)[/]*", user.HomeHandler),
    (r"/([A-Za-z0-9%_]+)/(topics|replies)/(hot)[/]*", user.HomeHandler),
    (r".*", site.PageNotFoundHandler),
]
