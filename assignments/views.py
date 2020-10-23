from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
# from django.contrib import messages
from django.views import generic
from django.shortcuts import get_object_or_404
from users.models import User
from assignments.models import Assignment, SubmitAssignment
from assignments.forms import GradeAssignmentForm, CreateAssignmentForm, SubmitAssignmentForm
from courses.models import Course

# Create your views here.    
class CreateAssignment(LoginRequiredMixin, generic.CreateView):
    form_class = CreateAssignmentForm
    template_name = 'assignments/create_assignment_form.html'
    # success_url = reverse('assignments/list/')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class AssignmentDetail(generic.DetailView):
    model = Assignment

    def get_context_data(self, **kwargs):
        course_obj = Course.objects.filter(students=self.request.user.id)
        context = super(AssignmentDetail, self).get_context_data(**kwargs)
        context['course'] = course_obj
        self.request.session['assignment'] = self.kwargs['pk']
        # print(self.request.session['assignment'])
        return context

class UpdateAssignment(LoginRequiredMixin, generic.UpdateView):
    model = Assignment
    form_class = CreateAssignmentForm
    template_name = 'assignments/create_assignment_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class DeleteAssignment(LoginRequiredMixin, generic.DeleteView):
    model = Assignment
    success_url = reverse_lazy('courses:list')

class SubmitAssignmentView(LoginRequiredMixin, generic.CreateView):
    form_class = SubmitAssignmentForm
    template_name = 'assignments/submitassignment_form.html'
    # model = SubmitAssignment
    # fields = ('topic', 'description', 'assignment_file', 'assignment_ques')
    select_related = ('author', 'assignment_ques')

    # def get_context_data(self, **kwargs):
    #     course_obj = Course.objects.filter(students=self.request.user.id)
    #     context = super(SubmitAssignmentView, self).get_context_data(**kwargs)
    #     context['course'] = course_obj
    #     return context

    # def form_valid(self, form):
    #     self.object = form.upload(commit=False)
    #     self.object.user = self.request.user
    #     self.object.save()
    #     return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['assignment_id'] = self.request.session.get('assignment')
        kwargs['user'] = self.request.user
        print(kwargs)
        return kwargs