import { useState } from 'react';

export default function StudentProfile() {

  const [profile, setProfile] = useState({ name: '', email: '', semester: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="profile-form">
      <h3>Student Profile</h3>
      <input name="name" placeholder="Name" onChange={handleChange} />
      <input name="email" placeholder="Email" onChange={handleChange} />
      <input name="semester" placeholder="Semester" onChange={handleChange} />
      <p>Preview: {profile.name} - {profile.semester}</p>
    </div>
  );
}