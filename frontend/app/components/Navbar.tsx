import Link from "next/link";



const Navbar = () => {

  const navItems = [
    {
      id:1,
      title:"Home",
      href:"/",
    },
    {
      id:2,
      title:"Runs",
      href:"/runs",
    },
    {
      id:3,
      title:"Challenges",
      href:"/challenges",
    },
    {
      id:4,
      title:"Forums",
      href:"/forums",
    },
    {
      id:5,
      title:"Help",
      href:"/help",
    },

  ]

  return (
    <div className='w-full h-16 bg-bg-dark flex justify-center'>
        <div className='w-6xl flex items-center gap-6 px-6'>
            <div className="flex gap-6">
              {navItems.map((item) => (
                <Link key={item.id} href={item.href}>
                  <span className="text-xl font-bold">{item.title}</span>
                </Link>
              ))}

            </div>
            <input placeholder="Search..." type="text" className="bg-bg-light rounded-2xl p-2  w-sm"/>
        </div>
    </div>
  )
}

export default Navbar;
