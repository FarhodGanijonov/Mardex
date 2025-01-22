from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CategoryJob, Job, City, Region
from .serializer import CategoryJobSerializer, JobSerializer, CitySerializer, RegionSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def category_job_list(request):
    category_jobs = CategoryJob.objects.all()
    serializer = CategoryJobSerializer(category_jobs, many=True, context={'request': request})
    return Response(serializer.data)


class JobListByCategoryView(APIView):
    def get(self, request, pk):
        category_job = get_object_or_404(CategoryJob, id=pk)
        jobs = Job.objects.filter(category_job=category_job)
        category_serializer = CategoryJobSerializer(category_job, context={'request': request})
        jobs_serializer = JobSerializer(jobs, many=True, context={'request': request})

        result = category_serializer.data
        result['jobs'] = jobs_serializer.data

        return Response(result)


@api_view(['GET'])
def job_list(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def job_similar(request, pk):
    job = get_object_or_404(Job, pk=pk)
    serializer = JobSerializer(job, context={'request': request})
    return Response(serializer.data)



@api_view(['GET'])
def city_list(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def city_count(request):
    count = City.objects.count()
    return Response({"cities_count": count})


@api_view(['GET'])
def region_list(request):
    regions = Region.objects.all()
    serializer = RegionSerializer(regions, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(['GET'])
def region_in_city(request, pk):
    try:
        city = City.objects.get(id=pk)  # Shaharning mavjudligini tekshirish
    except City.DoesNotExist:
        raise NotFound(detail="Shahar topilmadi.")  # Xato xabarini yuborish

    # city_id ni ishlatish kerak bo'lsa
    regions = Region.objects.filter(city_id=city.id)  # Shaharga bog'liq mintaqalarni olish
    serializer = RegionSerializer(regions, many=True, context={'request': request})
    return Response(serializer.data)


