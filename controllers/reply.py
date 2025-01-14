# coding: utf-8

import tornado.web

import config
from ._base import BaseHandler
from pony.orm import *

from models import Topic, Reply
from forms import ReplyForm
from .user import EmailMixin
from helpers import require_admin, require_permission

config = config.rec()


class HomeHandler(BaseHandler, EmailMixin):
    @db_session
    def get(self, reply_id):
        reply_id = int(reply_id)
        reply = Reply.get(id=reply_id)
        if not reply:
            raise tornado.web.HTTPError(404)
        return self.render("reply/index.html", reply=reply)

    @db_session
    @tornado.web.authenticated
    def put(self, reply_id):
        reply_id = int(reply_id)
        reply = Reply.get(id=reply_id)
        if not reply:
            raise tornado.web.HTTPError(404)
        action = self.get_argument('action', None)
        user = self.current_user
        if not action:
            result = {'status': 'info', 'message':
                      '缺少 action 参数'}
        if action == 'up':
            if reply.user_id != user.id:
                result = user.up(reply_id=reply.id)
            else:
                result = {'status': 'info', 'message':
                          '不能为自己的评论投票'}
        if action == 'down':
            if reply.user_id != user.id:
                result = user.down(reply_id=reply.id)
            else:
                result = {'status': 'info', 'message':
                          '不能为自己的评论投票'}
        if action == 'collect':
            result = user.collect(reply_id=reply.id)
        if action == 'thank':
            result = user.thank(reply_id=reply.id)
        if action == 'report':
            result = user.report(reply_id=reply.id)
        return self.send_result(result)

    @db_session
    @tornado.web.authenticated
    def delete(self, reply_id):
        if not self.current_user.is_admin:
            return self.redirect_next_url()
        reply = Reply.get(id=reply_id)
        if not reply:
            return self.redirect_next_url()
        subject = "评论删除通知 - " + config.site_name
        template = (
            '<p>尊敬的 <strong>%(nickname)s</strong> 您好！</p>'
            '<p>您在主题 <strong><a href="%(topic_url)s">「%(topic_title)s」</a></strong>'
            '下的评论由于违反社区规定而被删除，我们以邮件的形式给您进行了备份，备份数据如下：</p>'
            '<div class="content">%(content)s</div>'
        ) % {'nickname': reply.author.nickname,
             'topic_url': config.site_url + reply.topic.url,
             'topic_title': reply.topic.title,
             'content': reply.content}
        self.send_email(self, reply.author.email, subject, template)
        reply.remove()
        result = {'status': 'success', 'message': '已成功删除'}
        return self.send_result(result)


class CreateHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    @require_permission
    def post(self):
        page = int(self.get_argument('page', 1))
        topic_id = int(self.get_argument('topic_id', 0))
        topic = Topic.get(id=topic_id)
        if not topic_id:
            result = {'status': 'error', 'message':
                      '无此主题，不能创建评论'}
            if self.is_ajax:
                return self.write(result)
            else:
                self.flash_message(result)
                return self.redirect_next_url()
        user = self.current_user
        form = ReplyForm(self.request.arguments)
        if form.validate():
            reply = form.save(user=user, topic=topic)
            reply.put_notifier()
            result = {'status': 'success', 'message': '评论创建成功',
                      'content': reply.content, 'name': reply.author.name,
                      'nickname': reply.author.nickname, 'author_avatar':
                      reply.author.get_avatar(size=48), 'author_url':
                      reply.author.url, 'author_name': reply.author.name,
                      'author_nickname': reply.author.nickname,
                      'reply_url': reply.url, 'created': reply.created,
                      'id': reply.id, 'floor': reply.floor}
            if self.is_ajax:
                return self.write(result)
            self.flash_message(result)
            return self.redirect(topic.url)
        data = dict(form=form, topic=topic,
                    category='index', page=page)
        return self.send_result_and_render(form.result, "topic/index.html", data)


class EditHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    @require_permission
    def get(self, reply_id):
        reply = Reply.get(id=reply_id)
        if not reply or (reply.author != self.current_user and not self.current_user.is_admin):
            return self.redirect_next_url()
        form = ReplyForm(content=reply.content)
        return self.render("reply/edit.html", form=form, reply=reply)

    @db_session
    @tornado.web.authenticated
    @require_permission
    def post(self, reply_id):
        reply = Reply.get(id=reply_id)
        if not reply or (reply.author != self.current_user and not self.current_user.is_admin):
            return self.redirect_next_url()
        user = self.current_user
        form = ReplyForm(self.request.arguments)
        if form.validate():
            reply = form.save(user=user, topic=reply.topic, reply=reply)
            reply.put_notifier()
            result = {'status': 'success', 'message': '评论修改成功',
                      'reply_url': reply.url}
            return self.send_result(result, reply.url)
        data = dict(form=form, reply=reply)
        return self.send_result_and_render(form.result, "reply/edit.html", data)


class HistoryHandler(BaseHandler):
    @db_session
    def get(self, reply_id):
        reply = Reply.get(id=reply_id)
        if not reply:
            return self.redirect_next_url()
        if not reply.histories:
            return self.redirect(reply.topic.url)
        return self.render("reply/history.html", reply=reply, histories=reply.histories)
