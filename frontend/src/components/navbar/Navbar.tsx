type Props = {
  setIsInfoModalOpen: (value: boolean) => void
}

export const Navbar = ({ setIsInfoModalOpen }: Props) => {
  return (
    <div className="navbar">
      <div className="navbar-content short:h-auto px-5"></div>
    </div>
  )
}
