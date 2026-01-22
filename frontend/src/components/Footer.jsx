function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="relative z-10 mt-auto border-t bg-white/5 backdrop-blur-md border-white/10">
      <div className="px-4 py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
          <div className="text-center sm:text-left">
            <p className="text-sm font-semibold text-white">Dataset Platform</p>
            <p className="text-xs text-gray-400">Upload, analyze & manage your datasets</p>
          </div>
          <div className="text-xs text-center text-gray-400 sm:text-right">
            <p>&copy; {currentYear} Dataset Platform. All rights reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
