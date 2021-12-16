from odoo import models, fields, api
from odoo.exceptions import UserError


class projectTask(models.Model):
    _inherit = 'project.task'

    def action_timer_start(self):
        """ check the other running project task if already running raise
        an error timesheet already in progress with task name and id
        otherwise create a task and start timer
               """
        other_running_tasks = self.search([('user_timer_id', '!=', False), ('user_timer_id.user_id', '=', self.env.user.id), ('id', '!=', self.id)])
        if other_running_tasks and any([x.is_timer_running for x in other_running_tasks.filtered(lambda t: t.user_timer_id).mapped('user_timer_id')]):
            name = other_running_tasks.name_get(self.name_get())
            raise UserError(f'There is a timesheet in progress on {name} task:')
        super(projectTask, self).action_timer_start()
