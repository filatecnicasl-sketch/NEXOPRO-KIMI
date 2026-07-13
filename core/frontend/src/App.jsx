import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

const Dashboard = () => (
  <div className="p-6">
    <h1 className="text-3xl font-bold text-zinc-900 tracking-tight">NexoPro Platform</h1>
    <p className="text-zinc-500 mt-2">Dashboard del Core</p>
    <div className="grid grid-cols-3 gap-4 mt-6">
      <Card title="Clientes" value="124" icon="Users" />
      <Card title="Proveedores" value="38" icon="Building" />
      <Card title="Facturas" value="56" icon="FileText" />
    </div>
  </div>
);

const Card = ({ title, value, icon }) => (
  <div className="bg-white border border-zinc-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow">
    <div className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">{title}</div>
    <div className="text-2xl font-bold text-zinc-900 mt-1">{value}</div>
  </div>
);

const Contactos = () => {
  const [contactos, setContactos] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    fetch('http://localhost:8000/api/contactos')
      .then(r => r.json())
      .then(data => { setContactos(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-zinc-900 tracking-tight">Contactos</h1>
        <button className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors">
          Nuevo Contacto
        </button>
      </div>
      {loading ? (
        <div className="text-zinc-500">Cargando...</div>
      ) : (
        <div className="bg-white border border-zinc-200 rounded-lg shadow-sm overflow-hidden">
          <table className="w-full">
            <thead className="bg-zinc-50/90 border-b border-zinc-200">
              <tr>
                <th className="text-left text-xs font-semibold text-zinc-500 uppercase tracking-wider px-4 py-3">Nombre</th>
                <th className="text-left text-xs font-semibold text-zinc-500 uppercase tracking-wider px-4 py-3">Tipo</th>
                <th className="text-left text-xs font-semibold text-zinc-500 uppercase tracking-wider px-4 py-3">NIF</th>
                <th className="text-left text-xs font-semibold text-zinc-500 uppercase tracking-wider px-4 py-3">Email</th>
              </tr>
            </thead>
            <tbody>
              {contactos.map(c => (
                <tr key={c.id} className="border-b border-zinc-100 hover:bg-zinc-50 transition-colors">
                  <td className="px-4 py-3 text-sm font-medium text-zinc-900">{c.nombre}</td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                      c.tipo === 'cliente' ? 'bg-emerald-50 text-emerald-700 ring-1 ring-emerald-600/20' : 'bg-amber-50 text-amber-700 ring-1 ring-amber-600/20'
                    }`}>
                      {c.tipo}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-zinc-600 font-mono">{c.nif}</td>
                  <td className="px-4 py-3 text-sm text-zinc-600">{c.email}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

const Login = () => (
  <div className="min-h-screen flex items-center justify-center bg-zinc-50">
    <div className="bg-white border border-zinc-200 rounded-lg shadow-sm p-8 w-full max-w-md">
      <h2 className="text-2xl font-bold text-zinc-900 tracking-tight mb-6">Iniciar sesión</h2>
      <form className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-zinc-700 mb-1">Email</label>
          <input type="email" className="w-full border border-zinc-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2" />
        </div>
        <div>
          <label className="block text-sm font-medium text-zinc-700 mb-1">Contraseña</label>
          <input type="password" className="w-full border border-zinc-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2" />
        </div>
        <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded-md text-sm font-medium transition-colors">
          Entrar
        </button>
      </form>
    </div>
  </div>
);

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-zinc-50">
        <nav className="bg-white border-b border-zinc-200 px-6 py-3">
          <div className="flex items-center gap-8">
            <div className="font-bold text-xl text-indigo-600 tracking-tight">NexoPro</div>
            <div className="flex gap-4 text-sm font-medium text-zinc-600">
              <Link to="/" className="hover:text-zinc-900 transition-colors">Dashboard</Link>
              <Link to="/contactos" className="hover:text-zinc-900 transition-colors">Contactos</Link>
            </div>
          </div>
        </nav>
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/contactos" element={<Contactos />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
