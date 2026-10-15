"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { Activity, Users, DollarSign, Target, ShieldAlert, CheckCircle2, TrendingUp, AlertTriangle } from "lucide-react";

// Mock Data
const data = [
  { name: 'Tháng 1', users: 4000, churn: 240 },
  { name: 'Tháng 2', users: 3000, churn: 139 },
  { name: 'Tháng 3', users: 2000, churn: 980 },
  { name: 'Tháng 4', users: 2780, churn: 390 },
  { name: 'Tháng 5', users: 1890, churn: 480 },
  { name: 'Tháng 6', users: 2390, churn: 380 },
];

const pieData = [
  { name: 'Ở lại', value: 73.5, color: '#10b981' },
  { name: 'Rời mạng', value: 26.5, color: '#ef4444' },
];

// --- Simple Aceternity Sparkles Component ---
const SparklesCore = () => {
  return (
    <div className="absolute inset-0 w-full h-full pointer-events-none">
      {[...Array(30)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-1 h-1 bg-blue-500 rounded-full"
          initial={{
            x: Math.random() * (typeof window !== 'undefined' ? window.innerWidth : 1000),
            y: Math.random() * 400,
            opacity: Math.random(),
            scale: Math.random() * 2,
          }}
          animate={{
            y: [null, Math.random() * 400],
            opacity: [null, 0.8, 0],
            scale: [null, Math.random() * 3, 0],
          }}
          transition={{
            duration: Math.random() * 3 + 2,
            repeat: Infinity,
            ease: "linear",
          }}
        />
      ))}
    </div>
  );
};

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 overflow-hidden font-sans selection:bg-blue-500/30">
      
      {/* Aceternity Hero Header */}
      <div className="relative h-[28rem] flex flex-col items-center justify-center bg-slate-950 border-b border-white/10">
        <div className="absolute inset-0 bg-grid-white/[0.02] bg-[size:50px_50px]" />
        <div className="absolute inset-0 flex items-center justify-center bg-slate-950 [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)]"></div>
        <SparklesCore />
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="z-10 text-center space-y-4 px-4"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-4">
            <span className="flex h-2 w-2 rounded-full bg-blue-500"></span>
            Nhóm 22 - HCMUTE
          </div>
          <h1 className="text-5xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-b from-neutral-50 to-neutral-400">
            Dự Báo & Trực Quan Hóa
            <br /> <span className="text-blue-500">Customer Churn</span>
          </h1>
          <p className="max-w-2xl mx-auto text-lg text-slate-400 mt-4">
            Hệ thống phân tích, chẩn đoán nguyên nhân và đưa ra giải pháp AI tối ưu nhằm bảo vệ tài sản doanh nghiệp.
          </p>
        </motion.div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Navigation Tabs (Shadcn Style) */}
        <div className="flex space-x-1 p-1 bg-slate-900 rounded-lg overflow-x-auto mb-8 border border-slate-800">
          {[
            { id: 'overview', label: '1. Tổng quan' },
            { id: 'diagnostic', label: '2. Chẩn đoán' },
            { id: 'prediction', label: '3. Dự báo AI' },
            { id: 'strategy', label: '4. Chiến lược & ROI' },
            { id: 'architecture', label: '5. Kiến trúc' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 px-4 py-2.5 text-sm font-medium rounded-md whitespace-nowrap transition-all ${
                activeTab === tab.id 
                  ? 'bg-blue-600 text-white shadow-sm' 
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Shadcn UI Cards Style Grid */}
        <motion.div 
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* KPI Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card title="Khách Hàng Kích Hoạt" icon={<Users className="w-5 h-5 text-blue-500" />} value="7,043" change="+20% from last month" />
                <Card title="Tỷ Lệ Churn" icon={<AlertTriangle className="w-5 h-5 text-red-500" />} value="26.5%" change="Critical Level" changeColor="text-red-400" />
                <Card title="Doanh Thu Bốc Hơi" icon={<DollarSign className="w-5 h-5 text-amber-500" />} value="$139,130" change="Monthly Recurring" changeColor="text-amber-400" />
                <Card title="Tỷ Lệ An Toàn" icon={<ShieldAlert className="w-5 h-5 text-emerald-500" />} value="73.5%" change="Retained Customers" changeColor="text-emerald-400" />
              </div>

              {/* Charts Section */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 p-6 rounded-xl border border-slate-800 bg-slate-900/50 backdrop-blur-sm">
                  <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                    <Activity className="w-5 h-5 text-blue-400" /> 
                    Biến động Churn theo thời gian
                  </h3>
                  <div className="h-72">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={data} />
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="p-6 rounded-xl border border-slate-800 bg-slate-900/50 backdrop-blur-sm">
                  <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                    <Target className="w-5 h-5 text-blue-400" /> 
                    Tỷ Lệ Churn Tổng Thể
                  </h3>
                  <div className="h-72">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={pieData}
                          innerRadius={60}
                          outerRadius={90}
                          paddingAngle={5}
                          dataKey="value"
                          stroke="none"
                        >
                          {pieData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip 
                          contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px' }}
                          itemStyle={{ color: '#f8fafc' }}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="flex justify-center gap-4 mt-2">
                    <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-emerald-500"></div><span className="text-sm">Ở lại</span></div>
                    <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-red-500"></div><span className="text-sm">Rời mạng</span></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'prediction' && (
            <div className="p-8 rounded-xl border border-slate-800 bg-slate-900/50 backdrop-blur-sm">
              <div className="text-center max-w-3xl mx-auto mb-10">
                <h2 className="text-3xl font-bold mb-4">Mô Hình Trí Tuệ Nhân Tạo (AI Prediction)</h2>
                <p className="text-slate-400 text-lg">Giả lập các trường hợp khách hàng (What-If Analysis) để dự đoán xác suất rời mạng theo thời gian thực.</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                <div className="space-y-6">
                  <div className="grid grid-cols-2 gap-4">
                    <InputGroup label="Thâm niên (tháng)" defaultValue="4" />
                    <InputGroup label="Cước hàng tháng ($)" defaultValue="89.5" />
                    <SelectGroup label="Loại hợp đồng" options={['Month-to-month', 'One year', 'Two year']} />
                    <SelectGroup label="Dịch vụ Internet" options={['Fiber optic', 'DSL', 'No']} />
                  </div>
                  <button className="w-full py-3 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-semibold transition-colors shadow-[0_0_20px_rgba(37,99,235,0.4)]">
                    Dự Đoán Rủi Ro
                  </button>
                </div>
                <div className="flex flex-col items-center justify-center p-8 border border-slate-800 rounded-xl bg-slate-950">
                  <div className="text-6xl font-bold text-red-500 mb-2 drop-shadow-[0_0_15px_rgba(239,68,68,0.5)]">78.5%</div>
                  <div className="text-xl font-medium text-slate-300">Nguy cơ Rời mạng (Cao)</div>
                  <p className="text-center text-slate-500 mt-4">Tài khoản này có nguy cơ cao trong chu kỳ thanh toán tiếp theo.</p>
                </div>
              </div>
            </div>
          )}

          {activeTab !== 'overview' && activeTab !== 'prediction' && (
            <div className="flex items-center justify-center h-64 rounded-xl border border-dashed border-slate-700">
              <p className="text-slate-500">Nội dung tab đang được xây dựng...</p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}

// Mini Components for mockup
const Card = ({ title, icon, value, change, changeColor = "text-emerald-400" }: any) => (
  <div className="p-6 rounded-xl border border-slate-800 bg-slate-900/50 backdrop-blur-sm transition-transform hover:-translate-y-1 hover:shadow-lg hover:shadow-blue-900/20">
    <div className="flex items-center justify-between mb-4">
      <h4 className="text-sm font-medium text-slate-400">{title}</h4>
      <div className="p-2 bg-slate-800/50 rounded-lg">{icon}</div>
    </div>
    <div className="text-3xl font-bold text-slate-50">{value}</div>
    <div className={`text-xs mt-2 font-medium ${changeColor}`}>{change}</div>
  </div>
);

const AreaChart = ({ data }: { data: any[] }) => (
  <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
    <defs>
      <linearGradient id="colorUsers" x1="0" y1="0" x2="0" y2="1">
        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
      </linearGradient>
    </defs>
    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
    <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
    <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px' }} />
    <Line type="monotone" dataKey="users" stroke="#3b82f6" strokeWidth={3} dot={false} />
  </LineChart>
);

const InputGroup = ({ label, defaultValue }: any) => (
  <div className="flex flex-col gap-2">
    <label className="text-sm font-medium text-slate-400">{label}</label>
    <input 
      type="text" 
      defaultValue={defaultValue}
      className="bg-slate-950 border border-slate-700 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-200"
    />
  </div>
);

const SelectGroup = ({ label, options }: any) => (
  <div className="flex flex-col gap-2">
    <label className="text-sm font-medium text-slate-400">{label}</label>
    <select className="bg-slate-950 border border-slate-700 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-200 appearance-none">
      {options.map((opt: string) => <option key={opt} value={opt}>{opt}</option>)}
    </select>
  </div>
);
