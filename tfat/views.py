from django.shortcuts import render
from django.views.generic import ListView
from tfat.models import Species, JoePublic, Report, Recovery, Encounter


class JoePublicListView(ListView):
    model = JoePublic

class SpeciesListView(ListView):
    model = Species

class ReportListView(ListView):
    model = Report

class RecoveryListView(ListView):
    model = Recovery

class EncounterListView(ListView):
    model = Encounter
