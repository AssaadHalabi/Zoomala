from django.urls import path
from .views import OpportunitiesListView, OpportunityCreateView, OpportunityDeleteView, OpportunityUpdateView, OpportunityDetailView


urlpatterns = [
    path('', OpportunitiesListView.as_view(), name='searchOpportunities' ),
    path("<int:id>/",OpportunityDetailView.as_view(),name="detailOpportunity"),
    path('opportunity_create/', OpportunityCreateView.as_view(), name='createOpportunities' ),
    path('<int:id>/update/', OpportunityUpdateView.as_view(), name='updateOpportunities' ),
    path('<int:id>/delete/', OpportunityDeleteView.as_view(), name='deleteOpportunities' )

]


app_name= "opportunities"