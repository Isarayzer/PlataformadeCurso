import React from 'react';
import { Link } from 'react-router-dom';
import {
  Video,
  BookOpen,
  Users,
  TrendingUp,
  Plus,
  Upload,
  Play,
  Clock,
  MoreVertical,
} from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

/**
 * Dashboard page component
 */
const Dashboard = () => {
  // Mock statistics data
  const stats = [
    {
      title: 'Total Courses',
      value: '24',
      change: '+12%',
      trend: 'up',
      icon: BookOpen,
      color: 'primary',
    },
    {
      title: 'Total Videos',
      value: '156',
      change: '+8%',
      trend: 'up',
      icon: Video,
      color: 'secondary',
    },
    {
      title: 'Total Students',
      value: '1,234',
      change: '+23%',
      trend: 'up',
      icon: Users,
      color: 'success',
    },
    {
      title: 'Completion Rate',
      value: '87%',
      change: '+5%',
      trend: 'up',
      icon: TrendingUp,
      color: 'warning',
    },
  ];

  // Mock recent courses
  const recentCourses = [
    {
      id: 1,
      title: 'Complete Web Development Bootcamp',
      thumbnail: 'https://via.placeholder.com/300x170',
      lessons: 45,
      duration: '12h 30m',
      status: 'published',
      students: 234,
    },
    {
      id: 2,
      title: 'React Advanced Patterns',
      thumbnail: 'https://via.placeholder.com/300x170',
      lessons: 32,
      duration: '8h 45m',
      status: 'draft',
      students: 0,
    },
    {
      id: 3,
      title: 'UI/UX Design Fundamentals',
      thumbnail: 'https://via.placeholder.com/300x170',
      lessons: 28,
      duration: '6h 20m',
      status: 'published',
      students: 567,
    },
  ];

  // Quick actions
  const quickActions = [
    {
      title: 'Create Course',
      description: 'Start building a new course',
      icon: Plus,
      link: '/courses/new',
      color: 'primary',
    },
    {
      title: 'Upload Video',
      description: 'Add videos to your library',
      icon: Upload,
      link: '/videos/upload',
      color: 'secondary',
    },
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-neutral-900 font-display">
            Dashboard
          </h1>
          <p className="text-neutral-600 mt-1">
            Welcome back! Here's what's happening with your courses.
          </p>
        </div>
      </div>

      {/* Statistics grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.title} className="relative overflow-hidden">
              {/* Background decoration */}
              <div className={`absolute top-0 right-0 w-24 h-24 bg-${stat.color}-100 rounded-full -mr-12 -mt-12 opacity-50`} />

              <div className="relative">
                <div className="flex items-center justify-between mb-4">
                  <div className={`p-3 bg-${stat.color}-100 rounded-lg`}>
                    <Icon className={`text-${stat.color}-600`} size={24} />
                  </div>
                  <div className="flex items-center gap-1 text-success-600 text-sm font-medium">
                    <TrendingUp size={16} />
                    <span>{stat.change}</span>
                  </div>
                </div>
                <h3 className="text-2xl font-bold text-neutral-900">
                  {stat.value}
                </h3>
                <p className="text-sm text-neutral-600 mt-1">{stat.title}</p>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Quick actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {quickActions.map((action) => {
          const Icon = action.icon;
          return (
            <Link key={action.title} to={action.link}>
              <Card hover className="h-full">
                <div className="flex items-center gap-4">
                  <div className={`p-4 bg-gradient-${action.color} rounded-xl`}>
                    <Icon className="text-white" size={28} />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-neutral-900">
                      {action.title}
                    </h3>
                    <p className="text-sm text-neutral-600">
                      {action.description}
                    </p>
                  </div>
                </div>
              </Card>
            </Link>
          );
        })}
      </div>

      {/* Recent courses */}
      <Card
        title="Recent Courses"
        actions={
          <Link to="/courses">
            <Button variant="ghost" size="sm">
              View All
            </Button>
          </Link>
        }
      >
        <div className="space-y-4">
          {recentCourses.map((course) => (
            <div
              key={course.id}
              className="flex items-center gap-4 p-4 rounded-lg border border-neutral-200 hover:border-primary-300 hover:bg-primary-50 transition-all cursor-pointer"
            >
              {/* Thumbnail */}
              <img
                src={course.thumbnail}
                alt={course.title}
                className="w-32 h-18 object-cover rounded-lg"
              />

              {/* Course info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="text-base font-semibold text-neutral-900 truncate">
                    {course.title}
                  </h4>
                  <Badge variant={course.status === 'published' ? 'success' : 'warning'}>
                    {course.status}
                  </Badge>
                </div>
                <div className="flex items-center gap-4 text-sm text-neutral-600">
                  <span className="flex items-center gap-1">
                    <Play size={14} />
                    {course.lessons} lessons
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock size={14} />
                    {course.duration}
                  </span>
                  <span className="flex items-center gap-1">
                    <Users size={14} />
                    {course.students} students
                  </span>
                </div>
              </div>

              {/* Actions */}
              <button className="p-2 text-neutral-400 hover:text-neutral-600 hover:bg-neutral-100 rounded-lg transition-colors">
                <MoreVertical size={20} />
              </button>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default Dashboard;
