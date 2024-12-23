# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import CategoryJob, Job, City, Region
# from .serializer import CategoryJobSerializer, JobSerializer, CitySerializer, RegionSerializer
#
#
# @api_view(['GET'])
# def category_job_list(request):
#     category_jobs = CategoryJob.objects.all()
#     serializer = CategoryJobSerializer(category_jobs, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def category_job_recent(request):
#     recent_category_jobs = CategoryJob.objects.all().order_by('-created_at')[:5]
#     serializer = CategoryJobSerializer(recent_category_jobs, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def job_list(request):
#     jobs = Job.objects.all()
#     serializer = JobSerializer(jobs, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def job_similar(request, pk):
#     job = Job.objects.get(id=pk)
#     similar_jobs = Job.objects.filter(category_job=job.category_job)
#     serializer = JobSerializer(similar_jobs, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def city_list(request):
#     cities = City.objects.all()
#     serializer = CitySerializer(cities, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def city_count(request):
#     count = City.objects.count()
#     return Response({"cities_count": count})
#
#
# @api_view(['GET'])
# def region_list(request):
#     regions = Region.objects.all()
#     serializer = RegionSerializer(regions, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def region_in_city(request, pk):
#     city = City.objects.get(id=pk)
#     regions = Region.objects.filter(city_id=city)
#     serializer = RegionSerializer(regions, many=True)
#     return Response(serializer.data)
#
#
#
#