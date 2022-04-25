from django.shortcuts import render
from django.views import View


class Home(View):
    def get(self, *args, **kwargs):
        return render(self.request, template_name='index.html')


class ProjectView(View):
    def get(self, *args, **kwargs):
        project_id = self.kwargs['pk']
        print(project_id)
        return render(self.request, template_name='project.html', context={'project_id': project_id})
