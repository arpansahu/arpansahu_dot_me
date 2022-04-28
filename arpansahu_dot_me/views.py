from django.shortcuts import render
from django.views import View


class Home(View):
    def get(self, *args, **kwargs):
        return render(self.request, template_name='index.html')


class ProjectDetailedView(View):
    def get(self, *args, **kwargs):
        project_id = self.kwargs['pk']
        template_name = f'modules/project_detailed/project{project_id}.html'
        return render(self.request, template_name=template_name, context={'project_id': project_id})
